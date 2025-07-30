from rest_framework import serializers
from .models import SearchHistory

class CitySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, required=True)

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['city', 'timestamp']