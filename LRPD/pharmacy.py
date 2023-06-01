
from multiprocessing import Value
from django.forms import IntegerField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from Hr.models import Employee
from Users.models import sendException
from Hr.views import RemoveSpecialCharacters, text_validation
# from .forms import LabTestsForm, RadiologyExamForm
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
from django.db.models import Case, When

#------------order medicine ---------------
def order_medicine(request):
     try:
        if request.user.has_perm('LRPD.   view_pharmacy_medicine'):
            medicine_category =Medicine_categories.objects.all()
            medicine = Medicine.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =MedicineOrder.objects.filter(
                    Q(Medicine_name__icontains = SearchQuery) |
                    Q(Status__icontains = SearchQuery)
                    
                )
            else:
                order =MedicineOrder.objects.all().order_by(
                    Case(
                        When(Status="Pending" , then=1),
                        When(Status="Approved",then=2)
                        
                    )
                    
                    
                )

            paginator = Paginator(order, DataNumber)
            Status = 'Approved'
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                'status' : Status,
                'medicine_category' :medicine_category,
                'medicine' :medicine
            }
            return render (request, 'pharmacy/order_medicine.html',context)
        else:
            return render(request, 'Hr/403.html')
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

#-----------order medicine ----------------
def manage_medicine_order(request, action):
    try:
        if request.user.has_perm('LRPD.   add_pharmacy_medicine'):
            if action == 'new_medicine_order':
                if request.method == 'POST':
                    # Get all data from the request
                
                    MedicineCategory = request.POST.get('MedicineCategory1')
                    medicine = request.POST.get('Medicine1')
                    Quantity = request.POST.get('Qty1')
                    available_qty = request.POST.get('available_qty1')

                    
                    if ',' in MedicineCategory:
                        MedicineCategory = [x for x in MedicineCategory.split(',')]
                        for med_category in range(0, len(MedicineCategory )):
                            if MedicineCategory[med_category] == '' or MedicineCategory[med_category]== 'null' or MedicineCategory[med_category] is None or MedicineCategory[med_category] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Medicine Category',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                    else:
                        if MedicineCategory == '' or MedicineCategory== 'null' or MedicineCategory is None or MedicineCategory == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Medicine Category',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                    if ',' in medicine:
                        medicine = [int(x) for x in medicine.split(',')]
                        for medicine_len in range(0, len(medicine )):
                            if medicine[medicine_len] == '' or medicine[medicine_len] == 'null' or medicine[medicine_len] is None or medicine[medicine_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Enter Medicine',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    # else means it's one element and check as usual
                    else:
                        medicine = [int(x) for x in medicine.split(',')]
                        if medicine == '' or medicine == 'null' or medicine is None or medicine == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Enter Medicine',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    Quantity = [int(x) for x in Quantity.split(',')]
                    for quantity_len in range(0, len(Quantity )):
                        if Quantity[quantity_len] == '' or Quantity[quantity_len] == 'null' or Quantity[quantity_len] is None or Quantity[quantity_len] == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Select Quantity',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if Quantity[quantity_len] > int (available_qty):
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Box must be less then avalible quentity .',
                                    'title': 'Quantity Mismatch!',
                                    'type': 'warning',
                                }
                            )
                
                Status = "Pending"    
                new_medicine_order = MedicineOrder(Status=Status)
                new_medicine_order.save()    
            
                
                Current_medicine_order = MedicineOrder.objects.get(pk=new_medicine_order.id) 
                
                    
                for (med,quantity) in zip(medicine, Quantity):
                        get_medicine = Medicine.objects.get(id=med)
                        # print(quantity)
                        new_medicine_order_details = MedicineOrderDetails(medicineOrderid_id=Current_medicine_order.id, Medicine_name_id=get_medicine.id, box=quantity)
                        new_medicine_order_details.save()
                    
                return JsonResponse(
                    {
                        'isError': False,
                        'Message': 'New Medicine Order has been created',
                        'title': 'Masha Allah !',
                        'type': 'success+',
                    }
                )
        else:
            return render(request, 'Hr/403.html')    
        #-------PLAA----------
        
            #------PLA END---       
            
        if action == "MedicineOderView":
            if request.method == 'POST':
                id = request.POST.get('order_id')
                
                new_medicine_order = MedicineOrder.objects.get(id = id)
                new_medicine_order_details = MedicineOrderDetails.objects.filter(medicineOrderid_id=new_medicine_order.id)
                new_medicine_order1 = []
                for index, order in enumerate(new_medicine_order_details):
                    new_medicine_order1.append({
                        'id': order.id,
                        'MedicineName': order.Medicine_name.Medicine_name,
                        'Quantity': order.box,
                        
                    })
                message = {
                    'OrderId': new_medicine_order.id,
                    'medicineOrder': new_medicine_order1,
                }
            return JsonResponse({'isError': False, 'Message': message}, status=200)



        if action == "manage_medicine_order_data":
                    if request.method == 'POST':
                        medicines = Medicine.objects.all()
                        medicines_category = Medicine_categories.objects.all()
                        medicine = []
                        medicine_category = []
                        for index, item in enumerate(medicines_category):
                            medicine_category.append({
                                'id': item.id,
                                'name': item.medicine_cat_name,
                            })
                        for index, item in enumerate(medicines):
                            medicine.append({
                                'id': item.id,
                                'name': item.Medicine_name,
                            })
                        message = {
                            'medicines': medicine,
                            'medicines_category': medicine_category,
                        }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
        if action == "get_category_medicine":
                if request.method == 'POST':
                        medicine_id = request.POST.get('MedicineCategory1')
                        get_medicine_id = Medicine.objects.filter(
                            Medicine_categories=medicine_id)
                    
                        message = []
                        for xmedicine in range(0, len(get_medicine_id)):

                            message.append({
                                'id': get_medicine_id[xmedicine].id,
                                'name': get_medicine_id[xmedicine].Medicine_name,
                                'total_quantity': get_medicine_id[xmedicine].box,
                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)
        if action == "get_available_medicine":
                if request.method == 'POST':
                        medicine_id = request.POST.get('Medicine')
                        medicine = Medicine.objects.filter(id=medicine_id)
                    
                        message = []
                        for xmedicine in range(0, len(medicine)):

                            message.append({
                            
                                'box': medicine[xmedicine].box,
                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)
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

#-----------medicine list -----------------
def medicine_list(request):
    try:
    
        if request.user.has_perm('LRPD.   view_pharmacy_medicine'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []
            Status = 'Approved'

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =pharmacy_medicine.objects.filter(
                    Q(Medicine_name__Medicine_name__icontains = SearchQuery)| 
                    Q(Expire_date__icontains = SearchQuery) |
                    Q(Medicine_categories__medicine_cat_name__icontains = SearchQuery) 
                    
                )
            else:
                order =pharmacy_medicine.objects.all()
                # order =pharmacy_medicine.objects.filter(Q(medicineOrderid__Status__icontains = Status) )
            # if MedicineOrderDetails.objects.filter:
            #             for med in MedicineOrderDetails:
            #                 old_med_box= med.Medicine_name.box
            #                 new_med_box = med.Quantity
            #                 total = old_med_box + new_med_box
            #                 total.save()
            # list1 = pharmacy_medicine.objects.get(id=order.id)
            # if list1.box ==0:
            #     list1.status = "Not Available"
            #     list1.save()
            # else:
            #     list1.save()
            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                
            }
            return render (request, 'pharmacy/medicine_list.html',context)
        else:
            return render(request, 'Hr/403.html')
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
    
    

#--------------doctor order paginition- ------------------
def doctor_order(request):
    # try:
        if request.user.has_perm('LRPD.view_pharmacy_medicine'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =MedicinesPrescription.objects.filter(
                    Q(Status__icontains = SearchQuery) |
                    Q(Ordered_by__icontains =SearchQuery)|
                    Q(Appointment__Patient__PatientFirstName__icontains = SearchQuery)
                    
                )
            else:
                order =MedicinesPrescription.objects.all().order_by(
                    Case(
                        When(Status="Pending" , then=1),
                        When(Status="Approved",then=2),
                        
   
                    ) ,
                    Case(
                        When(Ordered_by="Emergency Department", then=1),
                        When(Ordered_by="Inpatient Unit", then=2),
                        When(Ordered_by="Oupatient Unit", then=3),
                        
                    )
                    

                      
                )

            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Status = 'Approved'
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                'status' : Status,
            }
            return render (request, 'pharmacy/doctor_order.html',context)  
        else:
            return render(request, 'Hr/403.html')
    
    # except Exception as error:
    #     username = request.user.username
    #     name = request.user.first_name + ' ' + request.user.last_name
    #     sendException(
    #         request, username, name, error)
    #     message = {
    #         'title': 'Server Error!',
    #         'type': 'error',
    #         'isError': True,
    #         'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
    #     }
    #     return JsonResponse(message, status=200)


#--------dector order ----------------
#-----------------MANAGING DOCOTOR ORDER AND SUBTRACTING THE BOXSES AND TOTAL-----------------
@login_required(login_url='Login')
def Manage_doctor_order(request, action ):
    # try:
        if request.user.has_perm('LRPD. add_pharmacy_medicine'):
            if action == "get_doctor_order":
                if request.method == 'POST':
                    id = request.POST.get('order_id')
                    
                    doctor_order = MedicinesPrescription.objects.get(id = id)
                    doctor_order_details = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=doctor_order.id)
                    doctor_orders = []
                    message = {}
                    for index, order in enumerate(doctor_order_details):
                        doctor_orders.append({
                            'id': order.id,
                            'MedicineName': order.MedicineName.Medicine_name.Medicine_name,
                            'Quantity': order.Quantity,
                            'Dose': order.Dose,
                            'DoseInterval': order.DoseInterval,
                            'DoseDuration': order.DoseDuration,
                            
                        })
                    if doctor_order.Admission: 
                        if doctor_order.Admission.Admission_order.Visit: 

                            message = {
                            'OrderId': doctor_order.id,
                            'AppointId': doctor_order.Admission.Admission_order.Visit.id,
                            'Doctor': doctor_order.Admission.Admission_order.Visit.emergencytriage_set.first.Doctor.get_full_name(),
                            'PatientName': doctor_order.Admission.Admission_order.Visit.Patient.get_fullName(),
                            'PatientAge': doctor_order.Admission.Admission_order.Visit.Patient.PatientAge,
                            'PatientGender': doctor_order.Admission.Admission_order.Visit.Patient.PatientGender,
                            'PatientMobileNo': doctor_order.Admission.Admission_order.Visit.Patient.PatientMobileNo,
                            'PatientDistrict': doctor_order.Admission.Admission_order.Visit.Patient.PatientDistrict,
                            'PatientVillage': doctor_order.Admission.Admission_order.Visit.Patient.PatientVillage,
                            'Instructions': doctor_order.instructions,
                            'doctor_orders': doctor_orders,
                            'Status':doctor_order.Status

             
                    }
                        
                        else:
                         message = {
                            'OrderId': doctor_order.id,
                            'AppointId': doctor_order.Admission.Admission_order.Appointment.id,
                            'Doctor': doctor_order.Admission.Admission_order.Appointment.Doctor.get_full_name(),
                            'PatientName': doctor_order.Admission.Admission_order.Appointment.Patient.get_fullName(),
                            'PatientAge': doctor_order.Admission.Admission_order.Appointment.Patient.PatientAge,
                            'PatientGender': doctor_order.Admission.Admission_order.Appointment.Patient.PatientGender,
                            'PatientMobileNo': doctor_order.Admission.Admission_order.Appointment.Patient.PatientMobileNo,
                            'PatientDistrict': doctor_order.Admission.Admission_order.Appointment.Patient.PatientDistrict,
                            'PatientVillage': doctor_order.Admission.Admission_order.Appointment.Patient.PatientVillage,
                            'Instructions': doctor_order.instructions,
                            'doctor_orders': doctor_orders,
                            'Status':doctor_order.Status

             
                    }
                        
                        
                    elif  doctor_order.Appointment:
                        message = {
                            'OrderId': doctor_order.id,
                            'AppointId': doctor_order.Appointment.id,
                            'Doctor': doctor_order.Appointment.Doctor.get_full_name(),
                            'PatientName': doctor_order.Appointment.Patient.get_fullName(),
                            'PatientAge': doctor_order.Appointment.Patient.PatientAge,
                            'PatientGender': doctor_order.Appointment.Patient.PatientGender,
                            'PatientMobileNo': doctor_order.Appointment.Patient.PatientMobileNo,
                            'PatientDistrict': doctor_order.Appointment.Patient.PatientDistrict,
                            'PatientVillage': doctor_order.Appointment.Patient.PatientVillage,
                            'Instructions': doctor_order.instructions,
                            'doctor_orders': doctor_orders,
                            'Status':doctor_order.Status

             
                    }

                    else:
                         message = {
                            'OrderId': doctor_order.id,
                            'AppointId': doctor_order.Visit.id,
                            'Doctor': doctor_order.Visit.Doctor.get_full_name(),
                            'PatientName': doctor_order.Visit.Patient.get_fullName(),
                            'PatientAge': doctor_order.Visit.Patient.PatientAge,
                            'PatientGender': doctor_order.Visit.Patient.PatientGender,
                            'PatientMobileNo': doctor_order.Visit.Patient.PatientMobileNo,
                            'PatientDistrict': doctor_order.Visit.Patient.PatientDistrict,
                            'PatientVillage': doctor_order.Visit.Patient.PatientVillage,
                            'Instructions': doctor_order.instructions,
                            'doctor_orders': doctor_orders,
                            'Status':doctor_order.Status

                    }

                   


                   
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            
            if action == "get_approvers":
                if request.method == 'POST':
                    id = request.POST.get('OrderId')
                
                    Status = "Approved" 
                    medid= MedicinesPrescription.objects.get(id=id)
                    medid.Status = Status
                    medid.save()
                    type = "Dispensed"
                    med_details =MedicinePrescriptionDetials.objects.filter(PrescriptionNo=medid.id)
                    
                


                    for med in med_details:
                        patient_qty = med.Quantity
                        pharmacy_qty = med.MedicineName.Total_quantity
                        total =  pharmacy_qty - patient_qty
                        box_qty = med.MedicineName.quantity
                        item  = MedicineTransection.objects.filter(MedId=med.MedicineName.Medicine_name.id).first()

                        


                        pharmacy_tarnsaction = PharmacyTransection(PhMedId_id=med.MedicineName.id,Type=type,box=patient_qty,quantity= med.MedicineName.quantity,Total_quantity=patient_qty,manufacturing_date=item.manufacturing_date
                        ,BatchNO=item.BatchNO,supplier_price=item.supplier_price,Expire_date=item.Expire_date,status=item.status)
                        pharmacy_tarnsaction.save()
                        
                        new_box = total//box_qty
                    
                        if new_box > 0:
                            update_pharmcy = pharmacy_medicine.objects.get(id=med.MedicineName.id)
                            update_pharmcy.Total_quantity = total
                            update_pharmcy.box = new_box
                            update_pharmcy.save()
                        else:
                            zero_box = 0
                            update_pharmcy = pharmacy_medicine.objects.get(id=med.MedicineName.id)
                            update_pharmcy.Total_quantity = total
                            update_pharmcy.box = zero_box
                            update_pharmcy.save()
                        
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'Your request approved',
                                'title': "masha allah ! been updated",
                                'type': 'success',
                            }
                        ) 
                
        else:
            return render(request, 'Hr/403.html')
        
    # except Exception as error:
    #     username = request.user.username
    #     name = request.user.first_name + ' ' + request.user.last_name
    #     sendException(
    #         request, username, name, error)
    #     message = {
    #         'title': 'Server Error!',
    #         'type': 'error',
    #         'isError': True,
    #         'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
    #     }
    #     return JsonResponse(message, status=200)

#-------------view medicine ------------------
def view_medicine(request, pk):
    pharmacy_medicine_view = pharmacy_medicine.objects.get(id=pk)
    medicine_tarnsections = pharmacy_medicine.objects.all()
    transection_medicine_view = PharmacyTransection.objects.filter(PhMedId=pk)

    context = {'pharmcy_medicine': pharmacy_medicine_view,
               'id':pk,
               'transection' : transection_medicine_view,
               'medicine_tarnsections':medicine_tarnsections
               

    }

    
    return render(request, 'pharmacy/view_medicine.html', context)

@login_required
def Expaire_medicine_pharmacy(request):
    # try:
        if request.user.has_perm('LRPD. view_pharmacy_medicine'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []
            Status = 'Expired'
            type = 'expired'
            today = date.today()

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =PharmacyTransection.objects.filter(Expire_date__lte = today
                
                    # 
                )
                order =PharmacyTransection.objects.filter(
                 Q(PhMedId__Medicine_name__Medicine_name__icontains = SearchQuery))
            else:
                order =PharmacyTransection.objects.filter(Expire_date__lte = today)
                
            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                'type' : type,
                'Status': Status
            }
            return render(request, 'pharmacy/expire_medicnie_ph.html',context) 
        else:
            return render(request, 'Hr/403.html')
    # except Exception as error:
    #     username = request.user.username
    #     name = request.user.first_name + ' ' + request.user.last_name
    #     sendException(
    #         request, username, name, error)
    #     message = {
    #         'title': 'Server Error!',
    #         'type': 'error',
    #         'isError': True,
    #         'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
    #     }
    #     return JsonResponse(message, status=200)



def print_pharmacy(request):
     return render(request, 'pharmacy/print.html')

