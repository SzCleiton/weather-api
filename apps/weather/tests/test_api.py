from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class WeatherAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.weather_url = reverse('weather-api')

    @patch('apps.weather.views.OpenWeatherService.get_current_weather')
    def test_get_weather_success_and_cache(self, mock_get_weather):
        mock_get_weather.return_value = {"temp": 20, "city": "São Paulo"}
        
        # 1ª chamada
        response = self.client.get(self.weather_url, {'city': 'São Paulo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get_weather.assert_called_once()

        # 2ª chamada (deve vir do cache)
        response_cached = self.client.get(self.weather_url, {'city': 'São Paulo'})
        self.assertEqual(response_cached.status_code, status.HTTP_200_OK)
        mock_get_weather.assert_called_once() # Não deve ser chamada de novo

    def test_get_weather_missing_city_param(self):
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)