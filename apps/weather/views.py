from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import structlog

from .services.openweather_service import OpenWeatherService
from .models import SearchHistory
from .tasks import save_search_history_task
from .serializers import CitySerializer, HistorySerializer

logger = structlog.get_logger(__name__)

class WeatherAPIView(APIView):
    def get(self, request, *args, **kwargs):
        log = logger.bind(user_id=request.user.id)
        serializer = CitySerializer(data=request.query_params)
        if not serializer.is_valid():
            log.warning("weather_api.validation.failed", errors=serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data['city'].lower()
        log = log.bind(city=city)
        cache_key = f"weather_{city}"

        cached_data = cache.get(cache_key)
        if cached_data:
            log.info("weather_api.cache.hit", cache_key=cache_key)
            return Response(cached_data)

        log.info("weather_api.cache.miss", cache_key=cache_key)
        try:
            service = OpenWeatherService()
            weather_data = service.get_current_weather(city)
        except Exception:
            log.error("weather_api.service.failed", exc_info=True)
            return Response({"error": "Erro ao buscar dados do clima."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        cache.set(cache_key, weather_data, timeout=600)
        log.info("weather_api.cache.set", cache_key=cache_key)

        save_search_history_task.delay(city=city, user_id=request.user.id, request_data=weather_data)
        log.info("weather_api.history_task.sent")

        return Response(weather_data, status=status.HTTP_200_OK)

class HistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        history = SearchHistory.objects.all()[:10]
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data)