from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.salary_list, name='list'),
    path('generate/<int:employee_id>/<int:year>/<int:month>/', views.generate_salary, name='generate'),
    path('edit/<int:pk>/', views.edit_salary, name='edit'),
    path('delete/<int:pk>/', views.delete_salary, name='delete'),
    path('pdf/<int:pk>/', views.generate_pdf, name='pdf'),
]
