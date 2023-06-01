from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from Hr.models import Employee
from Users.models import sendException
from Hr.views import RemoveSpecialCharacters, text_validation
from .models import *
from APEN.models import Appointments
from Inventory.models import Medicine ,Medicine_categories, Equipment, Equipment_categories , MedicineTransection
from APEN.models import Appointments, MedicinePrescriptionDetials, MedicinesPrescription
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Users.models import Users
currentDate = date.today()

#------------------Doctor---------------------------

def doctor_list(request):
    try:
        # if request.user.has_perm('Hr.view_employee'):
        CheckSearchQuery = 'SearchQuery' in request.GET
        CheckDataNumber = 'DataNumber' in request.GET
        # Checkjobtitle = 'Jobtitle' in request.GET   
        # Jobtitle = 'All'
        DataNumber = 5           
        SearchQuery = ''
        EmployeeList = []


        # if Checkjobtitle:
        #    Jobtitle = request.GET['Jobtitle']

        # dataFiltering = {}
        # if Jobtitle != 'All':
        #     dataFiltering['title__id'] = Jobtitle
            

            
            

        if CheckDataNumber:
            DataNumber = int(request.GET['DataNumber'])

        if CheckSearchQuery:
            SearchQuery = request.GET['SearchQuery']
            EmployeeList = Employee.objects.filter(
                Q(title__name__icontains=SearchQuery)|
                Q(first_name__icontains=SearchQuery) |
                Q(id__icontains=SearchQuery) |
                Q(gender__icontains=SearchQuery),
                title__name = 'doctor'

            

                # **dataFiltering
                
                
        
            )
        else:
            EmployeeList = Employee.objects.filter(
                    title__name  = 'doctor'
                )

        paginator = Paginator(EmployeeList, DataNumber,  )
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        emplNumber = Employee.objects.filter(title__name = 'doctor')
        emplmu =  len(emplNumber)

        context = {

            'page_obj': page_obj,
            'SearchQuery': SearchQuery,
            'DataNumber': DataNumber,

            'pageTitle': 'Employee List',

            'employeeNumber': emplmu



        }
        return render(request, 'doctor/AllDoctorsList.html', context)

    # else:
    #     return render(request, 'Hr/404.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return render (request, 'doctor/AllDoctorsList.html')


def doctor_appointments(request):
    try:
        if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            CheckDate = 'dataDate' in request.GET
            DataNumber = 10
            dataDate = currentDate.strftime('%Y-%m-%d')
            SearchQuery = ''
            EmployeeList = []

            if CheckDate:
                dataDate = request.GET['dataDate']

                expand = [int(x) for x in dataDate.split('-')]
                dataDate = date(expand[0] , expand[1] , expand[2]).strftime('%Y-%m-%d')
                
                
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                if request.user.is_staff:
                    EmployeeList = Appointments.objects.filter(
                        Q(Patient__PatientFullName__icontains=SearchQuery) |
                        Q(Doctor_icontains=SearchQuery) |
                        Q(id__icontains=SearchQuery) |
                        Q(gender__icontains=SearchQuery), AppointmentDate=dataDate, Doctor=request.user.employee,
                    )
                else:
                    EmployeeList = Appointments.objects.filter(
                        Q(Patient__PatientFullName__icontains=SearchQuery) |
                        Q(Doctor_icontains=SearchQuery) |
                        Q(id__icontains=SearchQuery) |
                        Q(gender__icontains=SearchQuery), AppointmentDate=dataDate
                    )

            else:

                EmployeeList = Appointments.objects.filter(
                    AppointmentDate=dataDate)

            paginator = Paginator(EmployeeList, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'dataDate': dataDate,                
                'pageTitle': 'Employee List',



            }
            return render(request, 'doctor/my_appointment.html', context)

        else:
            return render(request, 'Hr/404.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return render(request, 'Hr/employee_profile.html', context)
    
