from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('add/', views.add_employee, name='add'),
    path('edit/<int:pk>/', views.edit_employee, name='edit'),
    path('delete/<int:pk>/', views.delete_employee, name='delete'),
]
