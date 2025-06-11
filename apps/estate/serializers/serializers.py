# serializers.py

from rest_framework import serializers
from apps.estate.models.gallery import AdvertisementGallery
from apps.estate.models.advertisement import Advertisement
from rest_framework import serializers
from ..utils.estate_utils import AdvancedModelFieldExtractor


class AdvertisementGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementGallery
        fields = ['large_image', 'medium_image', 'small_image', 'thumbnail_image']


class AdvertisementListSerializer(serializers.Serializer):
    def to_representation(self, instance):


        request = self.context.get('request')

        fields_to_extract = [
            'id',
            'title',
            'price',
            'createdAt',
            'propertyType.title',
            'advType.title',
            'city.name'
        ]

        extracted_data = AdvancedModelFieldExtractor.extract_fields(
            model_instance=instance,
            fields_to_extract=fields_to_extract,
            context={'request': request}
        )

        gallery_images = AdvertisementGallery.objects.filter(advertisement=instance)
        images = [request.build_absolute_uri(g.large_image.url) for g in gallery_images if g.large_image]

        return {
            'id': extracted_data.get('id'),
            'title': extracted_data.get('title'),
            'price': extracted_data.get('price'),
            'createdAt': extracted_data.get('createdAt'),
            'propertyType': extracted_data.get('propertyType.title'),
            'advType': extracted_data.get('advType.title'),
            'images': images,
            'city':extracted_data.get('city.name')
        }
