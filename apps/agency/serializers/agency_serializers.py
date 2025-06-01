from rest_framework import serializers
from ..models import Agency,RejectedAgency
from apps.user.models.user_model import User
from apps.core.models.location_model import Province,City
from ..models.agency_model import Manager,Consultant

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



class RejectAgencySerializer(serializers.ModelSerializer):
    agencyId = serializers.UUIDField(source='agency.id', write_only=True)

    class Meta:
        model = RejectedAgency
        fields = ['agencyId', 'text']
        extra_kwargs = {
            'text': {'required': True}
        }


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']

class ConsultantSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id')
    full_name = serializers.SerializerMethodField()
    mobile_number = serializers.CharField(source='user.mobileNumber')
    is_active = serializers.BooleanField(source='isActive')

    class Meta:
        model = Consultant
        fields = ['user_id', 'full_name', 'mobile_number', 'profile_image', 'is_active']

    def get_full_name(self, obj):
        return f"{obj.user.firstName} {obj.user.lastName}"

class ManagerSerializer(serializers.ModelSerializer):

    user_id = serializers.UUIDField(source='user.id')
    full_name = serializers.SerializerMethodField()
    mobile_number = serializers.CharField(source='user.mobileNumber')
    is_active = serializers.BooleanField(source='isActive')

    class Meta:
        model = Manager
        fields = ['user_id', 'full_name', 'mobile_number', 'profile_image', 'is_active']

    def get_full_name(self, obj):
        return f"{obj.user.firstName} {obj.user.lastName}"

class AgencyDetailSerializer(serializers.ModelSerializer):

    cities = CitySerializer(many=True)
    province = ProvinceSerializer()
    consultants = ConsultantSerializer(many=True, source='consultants.all')
    managers = ManagerSerializer(many=True, source='managers.all')
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = Agency
        fields = [
            'user',
            'name',
            'profileImage',
            'bannerImage',
            'logoImage',
            'licenceImage',
            'email',
            'address',
            'province',
            'cities',
            'bio',
            'timeWork',
            'status',
            'status_display',
            'createdAt',
            'updatedAt',
            'consultants',
            'managers'
        ]



class UpdateAgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Agency
        exclude = ['user', 'createdAt', 'updatedAt', 'status', 'name','profileImage','logoImage','licenceImage']  

    def validate_name(self, value):
        raise serializers.ValidationError("تغییر نام آژانس مجاز نیست.")