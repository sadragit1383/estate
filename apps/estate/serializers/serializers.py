# serializers.py

from rest_framework import serializers
from apps.estate.models.gallery import AdvertisementGallery
from apps.estate.models.advertisement import Advertisement
from ..utils.estate_utils import get_model_fields

class AdvertisementGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementGallery
        fields = ['large_image', 'medium_image', 'small_image', 'thumbnail_image']


class AdvertisementListSerializer(serializers.ModelSerializer):

    propertyType = serializers.SerializerMethodField()
    advType = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'price',
            'createdAt',
            'propertyType',
            'advType',
            'images',
        ]

    def get_propertyType(self, obj):

        if obj.propertyType:
            return obj.propertyType.parent.title if obj.propertyType.parent else obj.propertyType.title
        return None

    def get_advType(self, obj):
        # برگرداندن عنوان propertyType یا parent آن (اگر وجود دارد)
        if obj.propertyType:
            return obj.advType.title if obj.propertyType else obj.advType.title
        return None

    def get_images(self, obj):
        request = self.context.get('request')
        if not request:
            return []

        # برگرداندن لیست URL تصاویر با بررسی وجود فیلد large_image
        return [
            request.build_absolute_uri(img.large_image.url)
            for img in obj.advertisement_gallery.filter(is_active=True)
            if img.large_image
        ]