# views.py

from rest_framework.generics import ListAPIView
from apps.estate.models.advertisement import Advertisement
from ..serializers.serializers import AdvertisementListSerializer


class AdvertisementListView(ListAPIView):
    
    queryset = Advertisement.objects.filter(isActive=True).prefetch_related('advertisement_gallery', 'propertyType__parent')
    serializer_class = AdvertisementListSerializer
