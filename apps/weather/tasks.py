from celery import shared_task
from django.contrib.auth import get_user_model
from .models import SearchHistory

User = get_user_model()

@shared_task
def save_search_history_task(city: str, user_id: int, request_data: dict):
    user = User.objects.get(id=user_id) if user_id else None
    SearchHistory.objects.create(city=city, user=user, request_data=request_data)
    
    pks_to_keep = SearchHistory.objects.all().values_list('pk', flat=True)[:10]
    SearchHistory.objects.exclude(pk__in=list(pks_to_keep)).delete()