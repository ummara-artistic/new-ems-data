from django.db import models
from django.core.validators import MinValueValidator

class Employee(models.Model):
    EMPLOYEE_TYPES = [
        ('employee', 'Employee'),
        ('labor', 'Labor'),
    ]
    
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    joining_date = models.DateField()
    age = models.IntegerField(validators=[MinValueValidator(18)])
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']
