from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/', views.mark_attendance, name='mark'),
    path('edit/<int:pk>/', views.edit_attendance, name='edit'),
    path('delete/<int:pk>/', views.delete_attendance, name='delete'),
    path('monthly/<int:employee_id>/', views.monthly_report, name='monthly_report'),
    path('monthly/<int:employee_id>/<int:year>/<int:month>/', views.monthly_report, name='monthly_report_detailed'),
]
