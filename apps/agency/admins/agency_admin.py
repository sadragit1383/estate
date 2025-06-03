from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from ..models.agency_model import Agency, Consultant, Manager, RejectedAgency
from .agency_serializers import RejectedAgencySerializer, AgencySerializer, ConsultantSerializer, ManagerSerializer
from rest_framework.decorators import action
from .agency_serializers import RequestCollaborationAgencySerializer
from .filter import RequestCollaborationAgencyFilter
from ..models.requestagency_model import RequestCollaborationAgency
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.user.models.permissions.user_permission import IsAdmin

class AgencyAdminViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdmin]

    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status',
        'name',
        'email',
        'address',
        'province',
        'province__name',
        'cities',
        'cities__name',
        'createdAt',
        'updatedAt',
        'user',

    ]

    search_fields = ['name', 'email', 'address']
    ordering_fields = ['createdAt', 'name']


    @action(detail=True, methods=['get'])
    def confirm(self, request, pk=None):
        success, message = Agency.confirm_agency(pk)
        return Response({"status": "success" if success else "error", "message": message})

    @action(detail=True, methods=['get'])
    def reject(self, request, pk=None):
        agency = self.get_object()
        reason = request.GET.get("reason")
        if not reason:
            return Response({"status": "error", "message": "دلیل رد کردن وارد نشده است."}, status=400)
        agency.reject_agency(reason)
        return Response({"status": "success", "message": "آژانس با موفقیت رد شد."})

    @action(detail=True, methods=['get'])
    def deactivate_member(self, request, pk=None):
        agency = self.get_object()
        user_id = request.GET.get("user_id")
        if not user_id:
            return Response({"status": "error", "message": "شناسه کاربر اجباری است."}, status=400)
        try:
            agency.deactivate_member(user_id)
            return Response({"status": "success", "message": "عضو غیرفعال شد."})
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)



class ConsultantAdminViewSet(viewsets.ModelViewSet):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'user',
        'agency',
        'isActive',
        'createdAt',
        'updatedAt',
        'user__mobileNumber',
        'user__firstName',
        'user__lastName',
    ]
    search_fields = ['user__mobileNumber', 'user__firstName', 'user__lastName']



class ManagerAdminViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'user',
        'agency',
        'isActive',
        'createdAt',
        'updatedAt',
        'user__mobileNumber',
        'user__firstName',
        'user__lastName',
    ]
    search_fields = ['user__mobileNumber', 'user__firstName', 'user__lastName']


class RejectedAgencyAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RejectedAgency.objects.all()
    serializer_class = RejectedAgencySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {

        'createdAt': ['gte', 'lte', 'exact'],
    }
    ordering_fields = ['createdAt']



class RequestCollaborationAgencyAdminViewSet(viewsets.ModelViewSet):
    queryset = RequestCollaborationAgency.objects.select_related('agency', 'user')
    serializer_class = RequestCollaborationAgencySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RequestCollaborationAgencyFilter
    search_fields = ['agency__name', 'user__firstName', 'user__lastName']
    ordering_fields = ['createdAt', 'status', 'role']
    ordering = ['-createdAt']

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        response_msg = request.data.get('responseMessage', '')
        instance.accept(response_msg)
        return Response({'detail': 'درخواست تایید شد'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        instance = self.get_object()
        response_msg = request.data.get('responseMessage', '')
        instance.reject(response_msg)
        return Response({'detail': 'درخواست رد شد'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        instance = self.get_object()
        response_msg = request.data.get('responseMessage', '')
        instance.cancel(response_msg)
        return Response({'detail': 'درخواست لغو شد'}, status=status.HTTP_200_OK)