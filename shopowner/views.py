from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import User
from accounts.forms import EmployeeCreationForm
from django.contrib import messages

def dashboard_view(request):
    return render(request, 'shopowner/dashboard.html')

def employee_list(request):
    employees = User.objects.filter(role='salesperson')  # แสดงพนักงานขาย
    return render(request, 'shopowner/employee_list.html', {'employees': employees})

def create_employee_view(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create(username=username, password=password, role='salesperson')
            messages.success(request, "Employee created successfully!")
            return redirect('owner_dashboard')
    else:
        form = EmployeeCreationForm()

    return render(request, 'shopowner/create_employee.html', {'form': form})

def edit_employee(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # อัปเดตพนักงาน
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm(instance=employee)
    return render(request, 'shopowner/edit_employee.html', {'form': form})

def delete_employee(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        employee.delete()  # ลบพนักงาน
        return redirect('employee_list')
    return render(request, 'shopowner/confirm_delete.html', {'employee': employee})