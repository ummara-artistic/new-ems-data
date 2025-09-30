import os
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labor_management.settings')
django.setup()

from employees.models import Employee
from attendance.models import Attendance
from salary.models import SalaryRecord

def create_sample_data():
    """Create sample data for testing the system"""
    
    print("🔄 Creating sample employees...")
    
    # Sample employee data
    sample_employees = [
        {'name': 'Ahmed', 'last_name': 'Ali', 'age': 28, 'salary': 25000, 'type': 'labor'},
        {'name': 'Muhammad', 'last_name': 'Hassan', 'age': 32, 'salary': 30000, 'type': 'labor'},
        {'name': 'Fatima', 'last_name': 'Khan', 'age': 26, 'salary': 35000, 'type': 'employee'},
        {'name': 'Usman', 'last_name': 'Sheikh', 'age': 29, 'salary': 28000, 'type': 'labor'},
        {'name': 'Aisha', 'last_name': 'Ahmed', 'age': 31, 'salary': 40000, 'type': 'employee'},
        {'name': 'Omar', 'last_name': 'Malik', 'age': 25, 'salary': 22000, 'type': 'labor'},
        {'name': 'Zainab', 'last_name': 'Hussain', 'age': 27, 'salary': 33000, 'type': 'employee'},
        {'name': 'Bilal', 'last_name': 'Raza', 'age': 30, 'salary': 26000, 'type': 'labor'},
    ]
    
    employees = []
    for emp_data in sample_employees:
        employee, created = Employee.objects.get_or_create(
            name=emp_data['name'],
            last_name=emp_data['last_name'],
            defaults={
                'age': emp_data['age'],
                'salary': emp_data['salary'],
                'employee_type': emp_data['type'],
                'joining_date': datetime.now().date() - timedelta(days=random.randint(30, 365))
            }
        )
        employees.append(employee)
        if created:
            print(f"✓ Created employee: {employee.full_name}")
    
    print(f"📊 Created {len(employees)} employees")
    
    # Create sample attendance for the last 30 days
    print("🔄 Creating sample attendance records...")
    
    attendance_count = 0
    for i in range(30):  # Last 30 days
        date = datetime.now().date() - timedelta(days=i)
        
        for employee in employees:
            # 85% chance of being present
            if random.random() < 0.85:
                status = 'present'
                in_time = datetime.strptime('09:00', '%H:%M').time()
                out_time = datetime.strptime('17:00', '%H:%M').time()
                overtime = random.choice([0, 0, 0, 1, 2, 3]) if random.random() < 0.3 else 0
            elif random.random() < 0.1:
                status = 'half_day'
                in_time = datetime.strptime('09:00', '%H:%M').time()
                out_time = datetime.strptime('13:00', '%H:%M').time()
                overtime = 0
            else:
                status = 'absent'
                in_time = None
                out_time = None
                overtime = 0
            
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date,
                defaults={
                    'status': status,
                    'in_time': in_time,
                    'out_time': out_time,
                    'overtime_hours': overtime
                }
            )
            
            if created:
                attendance_count += 1
    
    print(f"📊 Created {attendance_count} attendance records")
    
    # Create sample salary records for current month
    print("🔄 Creating sample salary records...")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    salary_count = 0
    for employee in employees[:4]:  # Create salary for first 4 employees
        # Calculate attendance for current month
        month_attendance = Attendance.objects.filter(
            employee=employee,
            date__year=current_year,
            date__month=current_month
        )
        
        days_present = month_attendance.filter(status='present').count()
        days_absent = month_attendance.filter(status='absent').count()
        overtime_hours = sum([att.overtime_hours for att in month_attendance])
        
        # Calculate salary components
        basic_salary = float(employee.salary) * 0.8  # 80% of monthly salary
        overtime_amount = overtime_hours * 200  # Rs. 200 per hour
        tea_allowance = 1000
        deductions = days_absent * 500  # Rs. 500 per absent day
        dues = random.choice([0, 1000, -500, 2000]) if random.random() < 0.3 else 0
        
        total_salary = basic_salary + overtime_amount + tea_allowance - deductions + dues
        
        salary_record, created = SalaryRecord.objects.get_or_create(
            employee=employee,
            month=current_month,
            year=current_year,
            defaults={
                'basic_salary': basic_salary,
                'overtime_amount': overtime_amount,
                'tea_allowance': tea_allowance,
                'deductions': deductions,
                'dues': dues,
                'total_salary': total_salary,
                'days_present': days_present,
                'days_absent': days_absent,
                'overtime_hours': overtime_hours,
                'notes': f'Sample salary record for {employee.full_name}'
            }
        )
        
        if created:
            salary_count += 1
            print(f"✓ Created salary record for: {employee.full_name}")
    
    print(f"📊 Created {salary_count} salary records")
    
    print("\n🎉 Sample data creation completed!")
    print("📋 Summary:")
    print(f"   • {len(employees)} employees")
    print(f"   • {attendance_count} attendance records")
    print(f"   • {salary_count} salary records")
    print("\n🚀 You can now test the system with realistic data!")

if __name__ == "__main__":
    create_sample_data()
