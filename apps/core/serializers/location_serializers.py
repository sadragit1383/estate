from rest_framework import serializers
from ..models.location_model import Country, Province, City, Area,UserLocation

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'slug']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'slug']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'slug']




class UserLocationSerializer(serializers.ModelSerializer):
    city = serializers.IntegerField(write_only=True)
    area = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserLocation
        fields = ['city', 'area']

    def validate(self, data):
        city_id = data.get('city')
        area_id = data.get('area')

        try:
            area = Area.objects.select_related('city').get(id=area_id)
        except Area.DoesNotExist:
            raise serializers.ValidationError("محله انتخاب‌شده وجود ندارد.")

        if area.city.id != city_id:
            raise serializers.ValidationError("محله به شهر انتخاب‌شده تعلق ندارد.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        city_id = validated_data.get('city')
        area_id = validated_data.get('area')

        return UserLocation.objects.create(
            user=user,
            city_id=city_id,
            area_id=area_id
        )