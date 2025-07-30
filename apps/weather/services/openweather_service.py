import requests
from django.conf import settings
import structlog

logger = structlog.get_logger(__name__)

class OpenWeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENWEATHER_API_KEY
        if not self.api_key:
            logger.error("openweather.api_key.missing")
            raise ValueError("OpenWeatherMap API Key não foi configurada.")

    def get_current_weather(self, city: str) -> dict:
        params = {'q': city, 'appid': self.api_key, 'units': 'metric', 'lang': 'pt_br'}
        log = logger.bind(city=city, api_url=self.BASE_URL)
        log.info("openweather.request.started", params=params)
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            weather_data = response.json()
            log.info("openweather.request.success")
            return weather_data
        except requests.exceptions.HTTPError as e:
            log.error("openweather.request.failed", status_code=e.response.status_code, response_body=e.response.text, exc_info=True)
            raise
        except requests.exceptions.RequestException as e:
            log.error("openweather.request.connection_error", error=str(e), exc_info=True)
            raise