from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'employee_type', 'salary', 'joining_date', 'is_active']
    list_filter = ['employee_type', 'is_active', 'joining_date']
    search_fields = ['name', 'last_name']
