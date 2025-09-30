from django.db import models
from employees.models import Employee
from django.core.validators import MinValueValidator

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # <-- Add this if you want to track late minutes
    late_minutes = models.FloatField(default=0)  # in minutes
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee__name']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
    
    @property
    def total_hours(self):
        if self.in_time and self.out_time:
            from datetime import datetime, timedelta
            in_datetime = datetime.combine(self.date, self.in_time)
            out_datetime = datetime.combine(self.date, self.out_time)
            
            # Handle overnight shifts
            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)
            
            total_time = out_datetime - in_datetime
            return total_time.total_seconds() / 3600  # Convert to hours
        return 0


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class EmployeeAllowance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    daily_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # per day

    def __str__(self):
        return f"{self.employee.name} - {self.daily_allowance}"
