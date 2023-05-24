import math

from drone.models import Drone
from video.models import Video, VideoFrame
from .detect_track import VehicleTrackerSingleton
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max, Count
from django.db import transaction
import cv2
import os
import uuid
from django.conf import settings

# Create your views here.
from .models import VehicleFrame, Vehicle


class DeployAlgorithmView(APIView):
    """
    View to deploy the detection and tracking algorithm on a specific video.
    """

    def get(self, request, video_filename):
        """
        Retrieve and initiate the detection and tracking algorithm on the video with the provided id.
        """
        # video = get_object_or_404(Video, pk=video_id)
        tracker = VehicleTrackerSingleton.getInstance()
        # # result = "success"
        result, vehicles = tracker.process_video(video_filename)
        for vehicle in vehicles:
            vehicle_frame = VehicleFrame(
                track_id=int(vehicle[0]),
                video_filename=vehicle[1],
                video_frame_cnt=int(vehicle[2]),

                x1=int(vehicle[3]),
                x2=int(vehicle[4]),
                y1=int(vehicle[5]),
                y2=int(vehicle[6]),
                x_position=(int(vehicle[3]) + int(vehicle[4])) / 2,
                y_position=(int(vehicle[5]) + int(vehicle[6])) / 2,
            )
            vehicle_frame.save()
        # with open('testarray.txt', 'w') as file:
        #     # 将数组中的元素逐行写入文件
        #     for item in vehicles:
        #         file.write(str(item) + '\n')
        return Response({"message": "Detection and tracking started.", "result": result})


class MatchVehiclesView(APIView):
    def get(self, request, video_filename):
        frame_groups = VehicleFrame.objects.filter(video_filename=video_filename).values('video_filename', 'track_id').annotate(
            min_frame_cnt=Min('video_frame_cnt'),
            max_frame_cnt=Max('video_frame_cnt'),
            group_size=Count('id')
        )
        with transaction.atomic():
            for group in frame_groups:
                if group['group_size'] > 30:
                    frames = VehicleFrame.objects.filter(video_filename=group['video_filename'],
                                                         track_id=group['track_id']).order_by('video_frame_cnt')
                    print(group)
                    if len(frames) % 2 == 1:
                        vehicle_frame = frames[len(frames) // 2]
                    else:
                        # 如果组中的数据数量是偶数，就取中间两个数据的第一个
                        vehicle_frame = frames[len(frames) // 2 - 1]
                    print("choosed vehicle frame:")
                    print(vehicle_frame)
                    # vehicle_frame = VehicleFrame.objects.get(video_frame_cnt=image_frame_cnt,
                    #                                          track_id=group['track_id'],
                    #                                          video_filename=video_filename)
                    x1, x2, y1, y2 = (vehicle_frame.x1, vehicle_frame.x2, vehicle_frame.y1, vehicle_frame.y2)
                    cap = cv2.VideoCapture(os.path.join(settings.MEDIA_ROOT, 'videos', video_filename))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, vehicle_frame.video_frame_cnt-1)
                    ret, frame = cap.read()
                    cap.release()
                    crop_img = frame[y1:y2, x1:x2]  # 切割图片
                    img_filename = str(uuid.uuid4()) + '.jpg'
                    print(img_filename)
                    cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'vehicles', img_filename), crop_img)
                    # 为每组数据创建一个新的Vehicle对象
                    Vehicle.objects.create(
                        entry_frame_cnt=group['min_frame_cnt'],
                        departure_frame_cnt=group['max_frame_cnt'],
                        video_filename=group['video_filename'],
                        image=img_filename,
                        track_id=group['track_id'],
                        # 注意: 这里没有设置image字段，因为它并不在原始数据中
                    )

        return Response({"message": "Vehicles added."})

class CalculateSpeedView(APIView):
    def get(self, request, video_filename):
        vehicles = Vehicle.objects.filter(video_filename=video_filename)
        video = Video.objects.get(video_filename=video_filename)
        x_resolution = video.x_resolution
        drone_magnification = Drone.objects.get(id=video.drone_id).drone_magnification
        for vehicle in vehicles:
            vehicleframes = VehicleFrame.objects.filter(video_filename=vehicle.video_filename, track_id=vehicle.track_id).order_by('video_frame_cnt')
            prev_x = vehicleframes[0].x_position
            prev_y = vehicleframes[0].y_position
            max_speed = 0
            total_speed = 0
            for vehicleframe in vehicleframes:
                cur_x = vehicleframe.x_position
                cur_y = vehicleframe.y_position
                pixel_distance = get_distance((prev_x, prev_y), (cur_x, cur_y))
                print(vehicleframe)
                try:
                    videoframe = VideoFrame.objects.get(video_id=video.id, video_frame_cnt=vehicleframe.video_frame_cnt)
                    height = videoframe.frame_altitude
                    dzoom_ratio = videoframe.frame_dzoom_ratio
                    diff_time = videoframe.frame_diff_time
                    speed = (height * drone_magnification * dzoom_ratio / x_resolution * pixel_distance) / diff_time * 3600
                    vehicleframe.speed = speed
                    vehicleframe.save()
                    if max_speed < speed: max_speed = speed
                    total_speed += speed
                except:
                    print('skip one frame')
                prev_x = cur_x
                prev_y = cur_y
            avg_speed = total_speed / (len(vehicleframes)-1)
            vehicle.max_speed = max_speed
            vehicle.avg_speed = avg_speed
            vehicle.save()
        return Response({"message": "Vehicles Speed Calculated."})



def get_distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])