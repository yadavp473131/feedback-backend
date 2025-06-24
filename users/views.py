from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, EmployeeReport, Feedback
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import EmployeeReportSerializer, FeedbackSerializer


# Views Signup endpoint
class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Login endpoint
class LoginView(APIView):
    def post(self, request):
    
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "message": "Login successful",
                "access_token": access_token,
               "refresh_token": str(refresh),
                "username": user.username,
                "email": user.email,
                "name":user.name,
                "role": getattr(user, "role", "N/A")
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

# employee report end point when employee is logged
class EmployeeReportView(APIView):
    permission_classes = [IsAuthenticated]
    # To get previous work reports working
    def get(self, request):
        print(" print in Employee report ")  
        reports = EmployeeReport.objects.filter(employee=request.user).order_by('-submitted_at')
        serializer = EmployeeReportSerializer(reports, many=True)
        return Response(serializer.data)
        
    # To submit work report done by employee and submit to manager
    def post(self, request):
        serializer = EmployeeReportSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save(employee=request.user)
            # return Response({'message': 'Report submitted successfully!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=201)  # 👈 returns report_id too
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Team Members list end point when manager is logged
class TeamMemberListView(APIView):
    permission_classes = [IsAuthenticated]
    # To get team members list from managerview working
    def get(self, request):
        user = request.user
        if user.role != 'manager':
            return Response({'error': 'Only managers can view team members.'}, status=403)

        team_members = CustomUser.objects.filter(teamId=user.teamId)
        serializer = UserSignupSerializer(team_members, many=True)
        return Response(serializer.data)


#individual employee report end point when manager is logged
class EmployeeReportByManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        user = request.user

        if user.role != 'manager':
            return Response({'error': 'Only managers can view employee reports.'}, status=403)

        try:
            employee = CustomUser.objects.get(employeeId=employee_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=404)

        # Optional: Verify if this employee belongs to the manager
        # if employee.manager_id != user.id:
        #     return Response({'error': 'Unauthorized to view this employee\'s reports.'}, status=403)

        reports = EmployeeReport.objects.filter(employee=employee).order_by('-submitted_at')
        report_serializer = EmployeeReportSerializer(reports, many=True)

        # Build structured response
        data = {
            "employee": {
                "id": employee.employeeId,
                "name": employee.name,
                "email": employee.email,
                "teamId": employee.teamId,
            },
            "reports": report_serializer.data
        }

        return Response(data)

#individual employee feedbacks end point when manager is logged
class ManagerViewEmployeeFeedbacks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        if request.user.role != 'manager':
            return Response({'error': 'Only managers can view this.'}, status=403)

        try:
            employee = CustomUser.objects.get(employeeId=employee_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

        if employee.teamId != request.user.teamId:
            return Response({'error': 'Not your team member'}, status=403)

        feedbacks = Feedback.objects.filter(employee=employee).order_by('created_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        
        return Response(serializer.data)

# Manager can submit feedback
class SubmitFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'manager':
            return Response({'error': 'Only managers can submit feedback'}, status=403)

        data = request.data
        
        try:
            employee = CustomUser.objects.get(employeeId=data['employee_id'])
            report = EmployeeReport.objects.get(report_id=data['report_id'])
            
        except CustomUser.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)
        except EmployeeReport.DoesNotExist:
            return Response({'error': 'Report not found'}, status=404)

        feedback = Feedback.objects.create(
            employee=employee,
            manager=user,
            report=report,
            comment=data['comment'],
            sentiment=data['sentiment']
        )
        return Response(FeedbackSerializer(feedback).data, status=201)
        # return Response({'message': 'Feedback submitted successfully'})
    
#employees can see feedback timeline
class EmployeeFeedbackHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'employee':
            return Response({'error': 'Only employees can view this'}, status=403)

        feedbacks = Feedback.objects.filter(employee=request.user).select_related('report', 'manager')
        
        return Response(FeedbackSerializer(feedbacks, many=True).data)

# acknowldgement timeline
class AcknowledgeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id, employee=request.user)
            feedback.acknowledged = True
            feedback.save()
            return Response({'message': 'Feedback acknowledged'})
        except Feedback.DoesNotExist:
            return Response({'error': 'Feedback not found or access denied'}, status=404)
        
from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer


# To update feedback
class FeedbackUpdateView(generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

