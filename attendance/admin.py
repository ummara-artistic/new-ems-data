from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'in_time', 'out_time', 'overtime_hours']
    list_filter = ['status', 'date', 'employee__employee_type']
    search_fields = ['employee__name', 'employee__last_name']
    date_hierarchy = 'date'
