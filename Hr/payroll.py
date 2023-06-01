from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from .views import *
from .models import *
# from APEN.models import Specialities

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re

def view_payroll(request):
    try:
        if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Checkdepartment = 'depName' in request.GET
            Jobtitle = 'All'
            depName = 'All'
            DataNumber = 30
            SearchQuery = ''
            EmployeeList = []

            if Checkjobtitle:
                Jobtitle = request.GET['Jobtitle']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['job_type_id'] = Jobtitle

            if Checkdepartment:
                depName = request.GET['depName']

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            dataFilterings = {}
            if depName != 'All':
                dataFilterings['department_all_id'] = depName
            

            getdetpartment = JobDetails.objects.filter(**dataFilterings, is_active = True).values('employee_id').distinct()
            print(getdetpartment)
            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee.objects.filter(
                    Q(emp_number__icontains=SearchQuery) |
                    Q(job_type__name__icontains=SearchQuery) |
                    Q(first_name__icontains=SearchQuery) |
                    Q(father_name__icontains=SearchQuery) |
                    Q(last_name__icontains=SearchQuery) |
                    Q(emp_number__icontains=SearchQuery) |
                    Q(gender__icontains=SearchQuery),
                    **dataFiltering,
                    Employee_state="Approved",
                    is_terminated=False,
                    




                )
            else:
                EmployeeList = Employee.objects.filter(
                 Q(id__in = getdetpartment),**dataFiltering,     Employee_state="Approved", is_terminated=False)

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            emplNumber = Employee.objects.filter(
                Employee_state="Approved", is_terminated=False)

            emplmu = len(emplNumber)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,
                'pageTitle': 'Employee List',
                'job_types': Title.objects.all(),
                'alldep': Departments.objects.all(),
                'depName':depName,

                'employeeNumber': emplmu



            }
            return render(request,'Hr/payrolllist.html',context)


        else:
            return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)

  