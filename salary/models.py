from django.db import models
from employees.models import Employee
from django.core.validators import MinValueValidator
from decimal import Decimal

class SalaryRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tea_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    advance_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dues = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    days_present = models.IntegerField(default=0)
    days_absent = models.IntegerField(default=0)
    half_days = models.IntegerField(default=0)
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    late_penalty_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_late_days = models.IntegerField(default=0)  # <-- Added field
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month', 'employee__name']

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year}"
