# serializers.py
from rest_framework import serializers
from ...models.user_model import User, RoleUser, UserSecret, UserLogin


class RoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecret
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'

