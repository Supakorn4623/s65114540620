from django.urls import path
from .views import dashboard_view ,create_employee_view , employee_list,edit_employee, delete_employee

urlpatterns = [
    path('dashboard/', dashboard_view, name='owner_dashboard'),
    path('create_employee/', create_employee_view, name='create_employee'),
    path('employees/', employee_list, name='employee_list'),
    path('edit-employee/<int:pk>/', edit_employee, name='edit_employee'),  
    path('delete-employee/<int:pk>/', delete_employee, name='delete_employee')
]
