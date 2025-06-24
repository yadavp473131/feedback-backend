from rest_framework import serializers
from .models import CustomUser, EmployeeReport, Feedback
from django.contrib.auth.hashers import make_password


class FeedbackSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()
    report_id = serializers.CharField(source='report.report_id', read_only=True)
    report_date = serializers.DateTimeField(source='report.submitted_at', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'manager', 'report_id', 'report_date', 'comment', 'sentiment', 'acknowledged', 'created_at']
        # read_only_fields = ['id', 'employee', 'manager', 'report', 'acknowledged', 'created_at']


class EmployeeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeReport
        fields = '__all__'
        read_only_fields = ['employee', 'submitted_at', 'manager_feedback']


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'password', 'role', 'employeeId', 'managerId', 'teamId']
        extra_kwargs = {'password': {'write_only': True},
                        'employeeId':{'required':False},
                        'managerId':{'required':False},
                        'teamId':{'required':False}}
        
        

        def validate(self, attrs):
            try:
                print("inside ",attrs)
            except Exception as e:
                print(" Error Printing attr ",e)
            role = attrs.get('role')
            
            if role == 'employee':
                if not attrs.get('employeeId'):
                    raise serializers.ValidationError({
                        'employeeId': 'This field is required for employees.'
                    })
                # Make sure we don't expect manager_id
                attrs['managerId'] = None

            elif role == 'manager':
                if not attrs.get('managerId'):
                    raise serializers.ValidationError({
                        'manager_id': 'This field is required for managers.'
                    })
                # Make sure we don't expect employee_id
                attrs['employeeId'] = None

            else:
                raise serializers.ValidationError({
                    'role': 'Invalid role. Must be either "employee" or "manager".'
                })
        
            print(attrs)
            return attrs


    def create(self, validated_data):
        # validated_data['password'] = make_password(validated_data['password'])
        # return super().create(validated_data)
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            employeeId=validated_data.get('employeeId'),
            managerId=validated_data.get('managerId'),
            teamId=validated_data.get('teamId')
        )
        return user