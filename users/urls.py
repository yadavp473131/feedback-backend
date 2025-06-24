from django.urls import path
from .views import (SignupView, LoginView, TeamMemberListView, EmployeeReportView, 
                     EmployeeReportByManagerView, ManagerViewEmployeeFeedbacks, 
                     SubmitFeedbackView, FeedbackUpdateView,
                    EmployeeFeedbackHistoryView,
                    AcknowledgeFeedbackView)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup'),
    path("signin/", LoginView.as_view(),name='signin'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('team-members/', TeamMemberListView.as_view()), # To get team members list from manager view
    path('employee/report/', EmployeeReportView.as_view(), name='employee-report'), # To post current work repoert by employee to manager
    path('employee/report-submission-history/', EmployeeReportView.as_view(), name='employee-report-submission-history'), #To fetch previous work report feedback provided by manager
    path('manager/employee/<int:employee_id>/reports/', EmployeeReportByManagerView.as_view()), # Individual employee current and previous reports working fine
    path('manager/employee/<int:employee_id>/feedbacks/', ManagerViewEmployeeFeedbacks.as_view()), # Individual employee current and previous feedbacks
    path('manager/feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),# To submit feedback by manager to individual employee working
    path('employee/feedback-history/', EmployeeFeedbackHistoryView.as_view(), name='feedback-history'), # Employee can get feedback history provided by manger working fine
    path('employee/acknowledge-feedback/<int:feedback_id>/', AcknowledgeFeedbackView.as_view(), name='acknowledge-feedback'),  # Employee has acknowldged managers feedback
    path('manager/feedback/<int:pk>/', FeedbackUpdateView.as_view(), name='feedback-update'),
]
