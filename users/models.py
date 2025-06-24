from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=50, blank=True, null=True)
    employeeId = models.CharField(max_length=50, blank=True, null=True)
    managerId = models.CharField(max_length=50, blank=True, null=True)
    teamId = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    


class EmployeeReport(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    work_summary = models.TextField()
    description = models.TextField()
    judgment_parameters = models.JSONField(default=list)
    submitted_at = models.DateTimeField(auto_now_add=True)
    manager_feedback = models.TextField(blank=True, null=True)
    report_id = models.CharField(max_length=100, unique=True, editable=False, default='')  # 👈 Unique report ID

    def __str__(self):
        return f"{self.employee.username}'s report {self.report_id} on {self.submitted_at.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if not self.report_id:
            uid = uuid.uuid4().hex[:8].upper()
            self.report_id = f"RPT-{uid}"
        super().save(*args, **kwargs)

class Feedback(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_feedbacks')
    report = models.ForeignKey(EmployeeReport, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    comment = models.TextField()
    sentiment = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)  # 👈 For employee acknowledgment

    def __str__(self):
        return f"Feedback by {self.manager.username} to {self.employee.username} ({self.sentiment})"
