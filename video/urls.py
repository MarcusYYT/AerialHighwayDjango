from django.urls import path
from .views import VideoUploadView, SRTUploadView, VideoDetail, VideoFrameList

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video_upload'),
    path('srtupload/', SRTUploadView.as_view(), name='srt_upload'),
    path('<int:video_id>/', VideoDetail.as_view(), name='video-detail'),
    path('frame/<int:video_id>/', VideoFrameList.as_view(), name='videoframe-list'),
]
