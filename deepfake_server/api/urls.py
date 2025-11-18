from django.urls import path
from .views import predict_video

urlpatterns = [
    path('predict/', predict_video, name='predict'),
]
