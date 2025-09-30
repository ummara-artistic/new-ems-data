from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from attendance.models import Attendance
from salary.models import SalaryRecord
from django.db.models import Count, Q, Sum, Avg
from datetime import datetime, timedelta
from calendar import monthrange
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Hardcoded admin credentials
        if username == 'admin' and password == 'admin':
            # Create or get admin user
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={'is_staff': True, 'is_superuser': True}
            )
            if created:
                user.set_password('admin')
                user.save()
            
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')


from employees.models import Employee

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Get current date info
    today = datetime.now().date()
    current_month = today.month
    current_year = today.year
    
    # Basic statistics
    total_employees = Employee.objects.filter(is_active=True).count()
    total_labor = Employee.objects.filter(employee_type='labor', is_active=True).count()
    total_employees_type = Employee.objects.filter(employee_type='employee', is_active=True).count()
    
    # Today's attendance
    today_present = Attendance.objects.filter(date=today, status='present').count()
    today_absent = Attendance.objects.filter(date=today, status='absent').count()
    today_half_day = Attendance.objects.filter(date=today, status='half_day').count()
    
    # This month's statistics
    month_attendance = Attendance.objects.filter(
        date__year=current_year,
        date__month=current_month
    )
    
    month_present = month_attendance.filter(status='present').count()
    month_absent = month_attendance.filter(status='absent').count()
    month_overtime = month_attendance.aggregate(Sum('overtime_hours'))['overtime_hours__sum'] or 0
    
    # Salary statistics for current month
    month_salaries = SalaryRecord.objects.filter(month=current_month, year=current_year)
    total_salary_paid = month_salaries.aggregate(Sum('total_salary'))['total_salary__sum'] or 0
    avg_salary = month_salaries.aggregate(Avg('total_salary'))['total_salary__avg'] or 0
    
    # Recent employees (last 5)
    recent_employees = Employee.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Recent attendance records (last 10)
    recent_attendance = Attendance.objects.select_related('employee').order_by('-date', '-created_at')[:10]
    
    # Monthly attendance chart data (last 6 months)
    chart_data = []
    chart_labels = []
    
    for i in range(5, -1, -1):  # Last 6 months
        target_date = today.replace(day=1) - timedelta(days=i*30)
        target_month = target_date.month
        target_year = target_date.year
        
        month_name = target_date.strftime('%b %Y')
        chart_labels.append(month_name)
        
        month_stats = Attendance.objects.filter(
            date__year=target_year,
            date__month=target_month
        ).aggregate(
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            half_day=Count('id', filter=Q(status='half_day'))
        )
        
        chart_data.append({
            'month': month_name,
            'present': month_stats['present'] or 0,
            'absent': month_stats['absent'] or 0,
            'half_day': month_stats['half_day'] or 0
        })
    
    # Employee type distribution
    employee_distribution = {
        'labor': total_labor,
        'employee': total_employees_type
    }
    
    # Top performers (employees with highest attendance this month)
    top_performers = Employee.objects.filter(is_active=True).annotate(
        present_days=Count('attendance', filter=Q(
            attendance__date__year=current_year,
            attendance__date__month=current_month,
            attendance__status='present'
        ))
    ).order_by('-present_days')[:5]
    
    # Attendance rate calculation
    total_working_days = monthrange(current_year, current_month)[1] - 4  # Excluding Sundays
    attendance_rate = 0
    if total_employees > 0 and total_working_days > 0:
        expected_attendance = total_employees * total_working_days
        actual_attendance = month_present + (month_attendance.filter(status='half_day').count() * 0.5)
        attendance_rate = (actual_attendance / expected_attendance) * 100 if expected_attendance > 0 else 0
    
    context = {
        'total_employees': total_employees,
        'total_labor': total_labor,
        'total_employees_type': total_employees_type,
        'today_present': today_present,
        'today_absent': today_absent,
        'today_half_day': today_half_day,
        'month_present': month_present,
        'month_absent': month_absent,
        'month_overtime': month_overtime,
        'total_salary_paid': total_salary_paid,
        'avg_salary': avg_salary,
        'recent_employees': recent_employees,
        'recent_attendance': recent_attendance,
        'chart_data': json.dumps(chart_data),
        'chart_labels': json.dumps(chart_labels),
        'employee_distribution': json.dumps(employee_distribution),
        'top_performers': top_performers,
        'attendance_rate': round(attendance_rate, 1),
        'current_month_name': today.strftime('%B'),
        'current_year': current_year,
    }
    
    return render(request, 'dashboard.html', context)
