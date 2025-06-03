from rest_framework import serializers
from ..models.agency_model import Agency, Consultant, Manager, RejectedAgency
from ..models.requestagency_model import RequestCollaborationAgency


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
        read_only_fields = ('status', 'createdAt', 'updatedAt')

class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class RejectedAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectedAgency
        fields = '__all__'




class RequestCollaborationAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCollaborationAgency
        fields = '__all__'
