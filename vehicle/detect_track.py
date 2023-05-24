import os
import random
import cv2
import torch
from django.conf import settings
from django.core.files.base import ContentFile

# from .models import VehicleFrame
from ultralytics import YOLO
from .tracker import Tracker


class VehicleTracker:
    def __init__(self):
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        # self.video_path = video_path
        # self.video_out_path = video_out_path
        # self.vehicle_out_path = vehicle_out_path
        # self.cap = cv2.VideoCapture(self.video_path)
        # video_out_path = os.path.join(settings.MEDIA_ROOT, 'processed')
        # self.model_path = model_path
        self.model = None
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(30)]
        self.tracker = Tracker()

    def load_model(self, model_path):
        self.model = YOLO(model_path)

    def process_video(self, video_name):
        if not self.model:
            return "Model not loaded. Please load the model first.", None
        video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_name)
        if not os.path.exists(video_path):
            return "file not found", None
        cap = cv2.VideoCapture(video_path)
        vehicles = []
        ret, frame = cap.read()
        cnt = 0
        while ret:
            cnt += 1
            results = self.model(frame)
            for result in results:
                detections = []
                for r in result.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = r
                    if score <= 0.5: continue
                    x1 = int(x1)
                    x2 = int(x2)
                    y1 = int(y1)
                    y2 = int(y2)
                    class_id = int(class_id)
                    detections.append([x1, y1, x2, y2, score])
                if len(detections) > 0:
                    self.tracker.update(frame, detections)
                    for track in self.tracker.tracks:
                        bbox = track.bbox
                        x1, y1, x2, y2 = bbox
                        track_id = track.track_id
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                      (self.colors[track_id % len(self.colors)]), 5)
                        # vehicles.append([track_id, int(x1), int(y1), int(x2), int(y2)])
                        # _, jpeg_vehicle = cv2.imencode('.jpg', frame[y1:y2, x1:x2])
                        # image_data_vehicle = ContentFile(jpeg_vehicle.tobytes())
                        # image_name = f'{video_name}_{track_id}_{cnt}.jpg'
                        # vehicle_frame = VehicleFrame(
                        #     track_id=track_id,
                        #     video_filename=video_name,
                        #     video_frame_cnt=cnt,
                        #     x_position=(x1+x2)/2,
                        #     y_position=(y1+y2)/2,
                        #     x1=x1,
                        #     y1=y1,
                        #     x2=x2,
                        #     y2=y2,
                        # )
                        # vehicle_frame.track_id = track_id
                        # vehicle_frame.video_filename = video_name
                        # vehicle_frame.video_frame_cnt = cnt
                        # vehicle_frame.x_position=(x1+x2)/2
                        # vehicle_frame.y_position=(y1+y2)/2
                        # vehicle_frame.x1=x1
                        # vehicle_frame.x2=x2
                        # vehicle_frame.y1=y1
                        # vehicle_frame.y2=y2
                        # # vehicle_frame.image.save(image_name, image_data_vehicle, save=True)
                        # vehicle_frame.save()
                        vehicles.append((track_id, video_name, cnt,  x1, x2,  y1, y2))
                        # .views.save_vehicle_frame(track_id, video_name, cnt, x1, x2, y1, y2)
                else:
                    print(f"Skipping frame {cnt} due to empty or incorrectly formatted detections.")
            cv2.imshow('frame', cv2.resize(frame, (1280, 720)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()

        cap.release()
        cv2.destroyAllWindows()
        return "success", vehicles


class VehicleTrackerSingleton:
    instance = None

    @staticmethod
    def getInstance():
        if not VehicleTrackerSingleton.instance:
            VehicleTrackerSingleton.instance = VehicleTracker()
            VehicleTrackerSingleton.instance.load_model('v8best.pt')
        return VehicleTrackerSingleton.instance
