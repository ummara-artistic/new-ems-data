from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Attendance

from django.shortcuts import render
from django.db.models import Sum, Count, Q
from .models import Attendance, Employee
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, date, timedelta
from calendar import monthrange
from .models import Attendance
from employees.models import Employee

@login_required
def attendance_list(request):
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = date.fromisoformat(selected_date)
    else:
        selected_date = date.today()

    selected_employee = request.GET.get('employee', '')
    selected_status = request.GET.get('status', '')

    employees = Employee.objects.all()
    attendance_records = []

    for emp in employees:
        attendance_qs = Attendance.objects.filter(employee=emp, date=selected_date)
        if selected_status:
            attendance_qs = attendance_qs.filter(status=selected_status)
        attendance = attendance_qs.first()

        # Determine status for display
        if attendance:
            status_display = attendance.get_status_display()
            late_flag = False
            late_minutes = 0
            if attendance.in_time:
                shift_start = datetime.combine(selected_date, datetime.strptime("09:15", "%H:%M").time())
                actual_in = datetime.combine(selected_date, attendance.in_time)
                if actual_in > shift_start:
                    late_flag = True
                    late_minutes = (actual_in - shift_start).seconds // 60
        else:
            status_display = 'Not Marked'
            late_flag = False
            late_minutes = 0

        attendance_records.append({
            'employee': emp,
            'status': status_display,
            'in_time': attendance.in_time if attendance else None,
            'out_time': attendance.out_time if attendance else None,
            'overtime_hours': attendance.overtime_hours if attendance else 0,
            'notes': attendance.notes if attendance else '',
            'is_late': late_flag,
            'late_minutes': late_minutes,
            'attendance_obj': attendance,  # for edit/delete links
        })

    # Aggregate totals
    total_present = Attendance.objects.filter(date=selected_date, status='present').count()
    total_absent = Attendance.objects.filter(date=selected_date, status='absent').count()
    total_half_day = Attendance.objects.filter(date=selected_date, status='half_day').count()
    total_marked = total_present + total_absent + total_half_day
    total_late = Attendance.objects.filter(date=selected_date).exclude(in_time__isnull=True).count()
    total_overtime = Attendance.objects.filter(date=selected_date).aggregate(total=Sum('overtime_hours'))['total'] or 0

    context = {
        'employees': employees,
        'attendance_records': attendance_records,
        'selected_date': selected_date,
        'selected_employee': selected_employee,
        'selected_status': selected_status,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_half_day': total_half_day,
        'total_marked': total_marked,
        'total_late': total_late,
        'total_overtime': total_overtime,
    }
    return render(request, 'attendance/list.html', context)


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        date_str = request.POST.get('date')  # this comes as string
        status = request.POST.get('status')
        in_time = request.POST.get('in_time')
        out_time = request.POST.get('out_time')
        overtime_hours = request.POST.get('overtime_hours', 0)
        notes = request.POST.get('notes', '')
        
        employee = get_object_or_404(Employee, id=employee_id)

        # ✅ convert date string to Python date
        try:
            attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            attendance_date = datetime.now().date()
        
        # Create or update attendance record
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=attendance_date,   # ✅ correct type
            defaults={
                'status': status,
                'in_time': in_time if in_time else None,
                'out_time': out_time if out_time else None,
                'overtime_hours': float(overtime_hours) if overtime_hours else 0,
                'notes': notes,
            }
        )
        
        if not created:
            attendance.status = status
            attendance.in_time = in_time if in_time else None
            attendance.out_time = out_time if out_time else None
            attendance.overtime_hours = float(overtime_hours) if overtime_hours else 0
            attendance.notes = notes
            attendance.save()
        
        messages.success(request, f'Attendance marked for {employee.full_name}')
        return redirect('attendance:list')
    
    employees = Employee.objects.filter(is_active=True).order_by('name')
    today = datetime.now().date()
    
    context = {
        'employees': employees,
        'today': today,
    }
    
    return render(request, 'attendance/mark.html', context)


@login_required
def edit_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        attendance.status = request.POST.get('status')
        attendance.in_time = request.POST.get('in_time') if request.POST.get('in_time') else None
        attendance.out_time = request.POST.get('out_time') if request.POST.get('out_time') else None
        attendance.overtime_hours = float(request.POST.get('overtime_hours', 0))
        attendance.notes = request.POST.get('notes', '')
        attendance.save()
        
        messages.success(request, 'Attendance updated successfully!')
        return redirect('attendance:list')
    
    return render(request, 'attendance/edit.html', {'attendance': attendance})

@login_required
def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully!')
        return redirect('attendance:list')
    
    return render(request, 'attendance/delete.html', {'attendance': attendance})

@login_required
def monthly_report(request, employee_id, year=None, month=None):
    from calendar import monthrange
    from datetime import datetime, timedelta
    from .models import Attendance
    from employees.models import Employee

    employee = get_object_or_404(Employee, id=employee_id)
    today = datetime.now().date()

    year = int(request.GET.get('year', year if year else today.year))
    month = int(request.GET.get('month', month if month else today.month))
    
    days_in_month = monthrange(year, month)[1]

    attendance_records = Attendance.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month
    ).order_by('date')

    attendance_dict = {record.date.day: record for record in attendance_records}

    calendar_data = []
    total_present = total_absent = total_half_day = total_overtime = total_late_days = 0

    for day in range(1, days_in_month + 1):
        date_obj = datetime(year, month, day).date()
        attendance = attendance_dict.get(day)
        is_late = False
        late_minutes = 0
        overtime_hours = 0

        if attendance:
            # Count attendance status
            if attendance.status == 'present':
                total_present += 1
            elif attendance.status == 'absent':
                total_absent += 1
            elif attendance.status == 'half_day':
                total_half_day += 1

            # Overtime
            if attendance.overtime_hours:
                overtime_hours = attendance.overtime_hours
                total_overtime += overtime_hours

            # Late check: after 09:15
            if attendance.in_time:
                shift_start = datetime.combine(date_obj, datetime.strptime("09:15", "%H:%M").time())
                actual_in = datetime.combine(date_obj, attendance.in_time)
                if actual_in > shift_start:
                    is_late = True
                    total_late_days += 1
                    late_minutes = (actual_in - shift_start).seconds // 60

        calendar_data.append({
            'day': day,
            'date': date_obj,
            'attendance': attendance,
            'is_today': date_obj == today,
            'is_late': is_late,
            'late_minutes': late_minutes,
            'overtime_hours': overtime_hours,
        })

    # Previous/next month for navigation
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    context = {
        'employee': employee,
        'year': year,
        'month': month,
        'month_name': datetime(year, month, 1).strftime('%B'),
        'calendar_data': calendar_data,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_half_day': total_half_day,
        'total_overtime': total_overtime,
        'total_late_days': total_late_days,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }

    return render(request, 'attendance/monthly_report.html', context)
