from django.contrib import admin
from .models import SalaryRecord

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'year', 'total_salary', 'days_present', 'days_absent']
    list_filter = ['year', 'month', 'employee__employee_type']
    search_fields = ['employee__name', 'employee__last_name']
