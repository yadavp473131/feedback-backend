from django.contrib import admin
from .models import CustomUser, EmployeeReport, Feedback

# Register your models here.
admin.site.register(CustomUser)


@admin.register(EmployeeReport)
class EmployeeReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'employee', 'short_summary', 'submitted_at')
    search_fields = ('employee__username', 'report_id')
    list_filter = ('submitted_at',)

    def short_summary(self, obj):
        return (obj.work_summary[:50] + '...') if len(obj.work_summary) > 50 else obj.work_summary
    short_summary.short_description = 'Work Summary'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'manager', 'report', 'sentiment', 'created_at')
    search_fields = ('employee__username', 'manager__username', 'report__report_id')
    list_filter = ('sentiment', 'created_at')
