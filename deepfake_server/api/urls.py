from django.urls import path
from .views import predict_video, health

urlpatterns = [
    path('predict/', predict_video, name='predict'),
    path('health/', health, name='health'),  # Health check endpoint
]
