from django.urls import path
from .views import WeatherAPIView, HistoryAPIView

urlpatterns = [
    path('weather/', WeatherAPIView.as_view(), name='weather-api'),
    path('history/', HistoryAPIView.as_view(), name='history-api'),
]