from moviepy.editor import VideoFileClip
from rest_framework import views, status, generics
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from .models import Video, VideoFrame
from .serializers import VideoSerializer, VideoFrameSerializer
import os
from django.conf import settings
import re
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class VideoUploadView(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.data['file']
        clip = VideoFileClip(file_obj.temporary_file_path())
        x_resolution, y_resolution = clip.size  # This gives you the resolution

        # Create and save a new video instance
        video = Video(
            video_filename=file_obj.name,
            x_resolution=x_resolution,
            y_resolution=y_resolution,
            drone_id=request.data['drone_id'],
            # video_file=file_obj  # save the file to the Video instance
            # add other fields as necessary

        )
        video.save()

        file_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(os.path.join(file_path, file_obj.name), 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Serialize the video instance for the response
        serializer = VideoSerializer(video)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SRTUploadView(views.APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        srt_file = request.FILES['file']
        video_name = srt_file.name.split('.')[0] + '.mp4'  # assuming the name of the video file and srt file are the same
        video = Video.objects.get(video_filename=video_name)
        lines = srt_file.read().decode('utf-8')

        pattern = r'SrtCnt : (\d+), DiffTime : (\d+)ms\n([\d-]+\s[\d:.]+)\n.*\[dzoom_ratio: (\d+).*\[latitude: ([^]]+)\] \[longitude: ([^]]+)\] \[rel_alt: ([\d.]+)'

        matches = re.findall(pattern, lines)

        for match in matches:
            # print(match)
            srt_cnt, diff_time, datetimestr, dzoom_ratio, latitude, longitude, rel_alt = match
            # subtitle_data = SubtitleData(srt_cnt, diff_time, datetime, dzoom_ratio, latitude, longitude, rel_alt)
            frame_data = {
                "video": video.id,
                "video_frame_cnt": int(srt_cnt),
                "frame_diff_time": int(diff_time),
                "frame_datetime": datetime.strptime(datetimestr, '%Y-%m-%d %H:%M:%S.%f'),
                "frame_latitude": float(latitude),
                "frame_longitude": float(longitude),
                "frame_altitude": float(rel_alt),
                "frame_dzoom_ratio": float(dzoom_ratio)/10000
            }
            serializer = VideoFrameSerializer(data=frame_data)
            if serializer.is_valid():
                serializer.save()

        # update the video's start_datetime, video_latitude, video_longitude with the first frame's data
        first_frame = matches[0]
        video.start_datetime = datetime.strptime(first_frame[2], '%Y-%m-%d %H:%M:%S.%f')  # convert string to datetime
        video.video_latitude = float(first_frame[4])
        video.video_longitude = float(first_frame[5])
        video.save()

        return Response(status=status.HTTP_201_CREATED)


class VideoDetail(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'video_id'


class VideoFrameList(generics.ListAPIView):
    serializer_class = VideoFrameSerializer

    def get_queryset(self):
        """
        This view should return a list of all the video frames
        for the video as determined by the video_id portion of the URL.
        """
        video_id = self.kwargs['video_id']
        return VideoFrame.objects.filter(video_id=video_id).order_by('video_frame_cnt')