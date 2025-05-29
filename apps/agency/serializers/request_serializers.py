from rest_framework import serializers
from apps.user.models.user_model import User
from ..models.requestagency_model import RequestCollaborationAgency, Role

class CollaborationRequestSerializer(serializers.ModelSerializer):
    mobileNumber = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = RequestCollaborationAgency
        fields = ['mobileNumber', 'role', 'request_message']
        extra_kwargs = {
            'request_message': {'required': False, 'allow_blank': True}
        }

    def validate_mobileNumber(self, value):
        if not User.objects.filter(mobileNumber=value).exists():
            raise serializers.ValidationError("کاربری با این شماره موبایل وجود ندارد")
        return value





class CollaborationResponseSerializer(serializers.Serializer):
    """
    سریالایزر برای پاسخ دادن به درخواست همکاری
    """
    id = serializers.UUIDField(required=True, help_text="شناسه درخواست همکاری")
    responseType = serializers.ChoiceField(
        choices=['accepted', 'rejected'],
        required=True,
        help_text="نوع پاسخ: accepted یا rejected"
    )
    responseMessage = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True,
        help_text="پیام پاسخ (اختیاری)"
    )

    def validate_id(self, value):
        """
        بررسی وجود درخواست همکاری
        """
        try:
            request_obj = RequestCollaborationAgency.objects.get(id=value)
            if request_obj.status != 'pending':
                raise serializers.ValidationError("این درخواست قبلاً پاسخ داده شده است")
            return value
        except RequestCollaborationAgency.DoesNotExist:
            raise serializers.ValidationError("درخواست همکاری با این شناسه یافت نشد")