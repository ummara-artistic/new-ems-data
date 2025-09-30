from django.db import models
from employees.models import Employee
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

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
    overtime_hours = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )  # Removed MinValueValidator to allow negative values
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    late_minutes = models.FloatField(default=0)  # in minutes
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee__name']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
    
    @property
    def total_hours(self):
        """Calculate worked hours after deducting lunch and excluding Sundays."""
        if self.in_time and self.out_time:
            in_datetime = datetime.combine(self.date, self.in_time)
            out_datetime = datetime.combine(self.date, self.out_time)

            # Handle overnight shifts
            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)
            
            total_hours = (out_datetime - in_datetime).total_seconds() / 3600

            # Deduct lunch hours
            if self.date.weekday() == 6:  # Sunday (0=Monday, 6=Sunday)
                return 0
            elif self.date.weekday() == 4:  # Friday
                total_hours -= 1
            else:
                total_hours -= 0.5

            return round(total_hours, 2) if total_hours > 0 else 0
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
        return f"{self.employee.full_name} - {self.daily_allowance}"
