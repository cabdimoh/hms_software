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
from django.contrib.auth.decorators import login_required

# ------------------Laboratory---------------------------


def lab_equipment_order(request):
    try:
        if request.user.has_perm('LRPD.view_labequipmentorder'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            Lab_equipment_order_list = []
            Collected_by = Employee.objects.all()
            status = "Pending"
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                Lab_equipment_order_list = LabEquipmentOrder.objects.filter(
                    Q(Appointment__Patient__get_fullName__icontains=SearchQuery) |
                    Q(Doctor__get_full_name__icontains=SearchQuery)
                )
            else:
                Lab_equipment_order_list = LabEquipmentOrder.objects.filter(Q(Status__icontains=status))

            paginator = Paginator(Lab_equipment_order_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Item = Equipment.objects.all()
            ItemCategory = Equipment_categories.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Lab Equipment Order List',
                'collected_by': Collected_by,
                'Items': Item,
                'ItemCategory': ItemCategory,
            }
            return render(request, 'lab/lab-equipment-orders.html', context)
        else:
            return render(request, 'Hr/404.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)
def manage_lab_equipment_order(request, action):
    if action == 'new_lab_eq_order':
        if request.method == 'POST':
            if request.user.has_perm('LRPD.add_labequipmentorder'):
                # Get all data from the request
                ItemName = request.POST.get('ItemName')
                Quantity = request.POST.get('Quantity')
                if ItemName == '' or ItemName == 'null' or ItemName is None or ItemName == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Test Name',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )

                if Quantity == '' or Quantity == 'null' or Quantity is None or Quantity == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Test Unit',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                Status = "Pending"
                ordered_by = Users.objects.get(id=request.user.id)
                item_id = Equipment.objects.get(id=ItemName)
                new_lab_equipment_order = LabEquipmentOrder(Item = item_id, Quantity= Quantity, Status=Status,Ordered_by=ordered_by)
                new_lab_equipment_order.save()

                return JsonResponse(
                    {
                        'isError': False,
                        'Message': 'A Lab Equipment has been ordered',
                        'title': 'Masha Allah !',
                        'type': 'success+',
                    }
                )
            else:
                return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'You dont have permission to place lab equipment order',
                        'title': 'Access is Denied !',
                        'type': 'warning',

                    },
                )
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


    
