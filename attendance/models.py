from django.db import models
from employees.models import Employee
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
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    late_minutes = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee__name']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
    
    @property
    def total_hours(self):
        if self.in_time and self.out_time:
            in_datetime = datetime.combine(self.date, self.in_time)
            out_datetime = datetime.combine(self.date, self.out_time)

            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)
            
            total_hours = (out_datetime - in_datetime).total_seconds() / 3600

            if self.date.weekday() == 6:  # Sunday
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


# ===============================
# Employee Allowances / Loans / Festivals
# ===============================

class Allowance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.amount}"


class Loan(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.amount}"


class FestivalDeduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.deduction_amount}"


from django.db import models
from employees.models import Employee
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
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    late_minutes = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee__name']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
    
    @property
    def total_hours(self):
        if self.in_time and self.out_time:
            in_datetime = datetime.combine(self.date, self.in_time)
            out_datetime = datetime.combine(self.date, self.out_time)

            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)
            
            total_hours = (out_datetime - in_datetime).total_seconds() / 3600

            if self.date.weekday() == 6:  # Sunday
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


# ===============================
# Employee Allowances / Loans / Festivals
# ===============================

class Allowance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.amount}"


class Loan(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.amount}"


class FestivalDeduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year} - {self.deduction_amount}"


from django.db import models
from employees.models import Employee  # Correct import from employees app

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    month = models.PositiveSmallIntegerField()  # 1=Jan, 2=Feb, etc.
    year = models.PositiveSmallIntegerField()
    days = models.PositiveSmallIntegerField(default=0)  # Number of leave days

    class Meta:
        unique_together = ('employee', 'month', 'year')
        verbose_name = 'Monthly Leave'
        verbose_name_plural = 'Monthly Leaves'

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year}: {self.days} days"


class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Paid','Paid'),('Pending','Pending'),('Canceled','Canceled')], default='Pending')
