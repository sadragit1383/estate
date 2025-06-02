from django.urls import path
from .views.agency_view import UpdateAgencyAPIView,AgencyAPIView,AgencyConfirmationAPIView,RejectAgencyAPIView,AgencyCreateAPIView,CollaborationRequestAgencyAPIView,DeactivateAgencyMemberAPIView
from .views.request_view import CollaborationRequestAPIView,CollaborationRequestListAPIView,CollaborationResponseAPIView

urlpatterns = [

    path('create/agency', AgencyCreateAPIView.as_view()),
    path('agency/update', UpdateAgencyAPIView.as_view(), name='update_agency'),
    path('request/agency',CollaborationRequestAPIView.as_view()),
    path('request/userlist',CollaborationRequestListAPIView.as_view()),
    path('collaboration/respond', CollaborationResponseAPIView.as_view(), name='collaboration-respond'),
    path('listrequest/agency',CollaborationRequestAgencyAPIView.as_view()),
    path('agency/deactivemember', DeactivateAgencyMemberAPIView.as_view()),
    path('agency/reject', RejectAgencyAPIView.as_view()),
    path('agency/confirm', AgencyConfirmationAPIView.as_view()),
    path('getagency', AgencyAPIView.as_view(), name='my-agency'),

]
