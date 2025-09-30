from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from datetime import datetime


from .models import Employee
@login_required
def employee_list(request):
    employees = Employee.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Filter by employee type
    employee_type = request.GET.get('type')
    if employee_type:
        employees = employees.filter(employee_type=employee_type)
    
    now = datetime.now()
    context = {
        'employees': employees,
        'search_query': search_query,
        'employee_type': employee_type,
        'current_year': now.year,
        'current_month': now.month,
    }
    
    return render(request, 'employees/list.html', context)

@login_required
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        joining_date = request.POST.get('joining_date')
        age = request.POST.get('age')
        salary = request.POST.get('salary')
        employee_type = request.POST.get('employee_type')
        
        Employee.objects.create(
            name=name,
            last_name=last_name,
            joining_date=joining_date,
            age=age,
            salary=salary,
            employee_type=employee_type
        )
        
        messages.success(request, 'Employee added successfully!')
        return redirect('employees:list')
    
    return render(request, 'employees/add.html')

@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.last_name = request.POST.get('last_name')
        employee.joining_date = request.POST.get('joining_date')
        employee.age = request.POST.get('age')
        employee.salary = request.POST.get('salary')
        employee.employee_type = request.POST.get('employee_type')
        employee.save()
        
        messages.success(request, 'Employee updated successfully!')
        return redirect('employees:list')
    
    return render(request, 'employees/edit.html', {'employee': employee})

@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employees:list')
    
    return render(request, 'employees/delete.html', {'employee': employee})
