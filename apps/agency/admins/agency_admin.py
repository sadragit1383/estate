from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from ..models.agency_model import Agency, Consultant, Manager, RejectedAgency
from .agency_serializers import RejectedAgencySerializer, AgencySerializer, ConsultantSerializer, ManagerSerializer

class AgencyAdminViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'name': ['exact', 'icontains'],
        'province__name': ['exact'],
        'cities__name': ['exact'],
        'createdAt': ['gte', 'lte', 'exact'],
    }
    search_fields = ['name', 'email', 'address']
    ordering_fields = ['createdAt', 'name']

    @action(detail=True, methods=['get'])
    def confirm(self, request, pk=None):
        """تایید آژانس با GET"""
        agency = self.get_object()
        success, message = Agency.confirm_agency(agency.pk)
        if success:
            return Response({'status': 'confirmed'}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reject(self, request, pk=None):
        """رد آژانس با GET و دریافت دلیل از query parameters"""
        reason = request.query_params.get('reason', '')
        if not reason:
            return Response({'error': 'پارامتر reason الزامی است'},
                          status=status.HTTP_400_BAD_REQUEST)

        agency = self.get_object()
        agency.reject_agency(reason)
        RejectedAgency.objects.create(agency=agency, text=reason)
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def deactivate_member(self, request, pk=None):
        """غیرفعال کردن عضو با GET و دریافت user_id از query parameters"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'پارامتر user_id الزامی است'},
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            agency = self.get_object()
            agency.deactivate_member(user_id)
            return Response({'status': 'member deactivated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConsultantAdminViewSet(viewsets.ModelViewSet):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {

        'isActive': ['exact'],
        'user__mobileNumber': ['exact'],
    }
    search_fields = ['user__mobileNumber', 'user__firstName', 'user__lastName']


class ManagerAdminViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {

        'isActive': ['exact'],
        'user__mobileNumber': ['exact'],
    }
    search_fields = ['user__mobileNumber', 'user__firstName', 'user__lastName']


class RejectedAgencyAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RejectedAgency.objects.all()
    serializer_class = RejectedAgencySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {

        'createdAt': ['gte', 'lte', 'exact'],
    }
    ordering_fields = ['createdAt']