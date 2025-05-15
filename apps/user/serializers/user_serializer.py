from rest_framework import serializers
from ..models.user_model import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('mobile_number', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password']
        )
