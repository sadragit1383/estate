from rest_framework import serializers
from ..models import Agency
from apps.user.models.user_model import User

class AgencyCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    location_slugs = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Agency
        fields = [
            'user', 'name', 'address', 'email', 'bio', 'timeWork',
            'location_slugs', 'profileImage', 'licenceImage',
            'bannerImage', 'logoImage'
        ]
        extra_kwargs = {
            'profileImage': {'required': False},
            'licenceImage': {'required': False},
            'bannerImage': {'required': False},
            'logoImage': {'required': False},
        }

