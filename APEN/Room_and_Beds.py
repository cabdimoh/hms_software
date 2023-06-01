from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from Hr.views import RemoveSpecialCharacters
from .models import Appointments, AssignBed, Patients, MedicinesPrescription,MedicinePrescriptionDetials, Specialities, OperationCategory, Operations, Patient_operation , Room_category,Room,Beds
from Hr.models import Employee, Title, JobType,Departments
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Inventory.models import Medicine, Medicine_categories
from LRPD.models import LabTests, LabTestOrders, RadiologyExam, RadiologyOrders, LabTestOrderDetails, RadiologyOrderDetails, LabTestResult, RadiologyResult,pharmacy_medicine
from LRPD.models import *
from Users.models import Users 
from django.contrib.auth.decorators import permission_required
from Users.models import sendException
from Users.views import sendTrials
from django.db.models import Sum

@login_required(login_url='Login')
def room_category(request):
    try:
        if request.user.has_perm('APEN.   view_room_category'):
            department = Departments.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            Room_category_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                Room_category_list =Room_category.objects.filter(
                    Q(Category_name__icontains = SearchQuery)    
                )
            else:
                Room_category_list =Room_category.objects.all()

            paginator = Paginator(Room_category_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Room category List',
                'department' : department 
            }
            return render(request, 'Rooms_and_beds/roomCategory.html',context)
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


def manage_room_category(request,action):
    try:
        if request.user.has_perm('APEN.   add_room_category'):
            if action == 'new_room_category':
            
                if request.method == 'POST':
                    # Get all data from the request
                    department_name = request.POST.get('department_name')
                    CategoryName = request.POST.get('CategoryName')
                    Description = request.POST.get('Description')
                    # Validaet dat
                    if department_name == '' or department_name == 'null' or department_name is None or department_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select department ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if CategoryName == '' or CategoryName == 'null' or CategoryName is None or CategoryName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter category name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Description == '' or Description == 'null' or Description is None or Description == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter discription ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                department_name=RemoveSpecialCharacters(department_name)
                CategoryName = RemoveSpecialCharacters(CategoryName)
                Description = RemoveSpecialCharacters(Description)

                # depatment_id = Departments.objects.get(id=CategoryName)
                new_room_category = Room_category(department_id=department_name , Category_name = CategoryName, Discription= Description)
                new_room_category.save()

                return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'new Category has been created',
                                'title': 'masha allah !',
                                'type': 'success+',
                            }
                        )
        else:
                return render(request, 'Hr/403.html')
            
        if request.user.has_perm('APEN.   change_room_category'):
            if action == 'update_room_category':
                    if request.method == 'POST':
                    # Get all data from the request
                        id = request.POST.get('id')
                        department_name = request.POST.get('department_name')
                        CategoryName = request.POST.get('CategoryName')
                        Description = request.POST.get('Description')
                            
                        # Validaet data
                        if department_name == '' or department_name == 'null' or department_name is None or department_name == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter department_name ',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if CategoryName == '' or CategoryName == 'null' or CategoryName is None or CategoryName == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter CategoryNamee ',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                        if Description == '' or Description == 'null' or Description is None or Description == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter Description',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                        Department = Departments.objects.get(id=department_name)
                        update_room_cat= Room_category.objects.get(id=id)
                        update_room_cat.department = Department
                        update_room_cat.Category_name = CategoryName
                        update_room_cat.Discription = Description
                        
                        update_room_cat.save()
                        return JsonResponse(
                            {
                                    'isError': False,
                                    'Message': 'an Room  Category has been updated',
                                    'title': 'masha allah !' + CategoryName + " been updated" ,
                                    'type': 'success',
                                }
                            )

        else:
                return render(request, 'Hr/403.html')
        
        if action == "getroomcat":
                if request.method == 'POST':
                    id = request.POST.get('id')
                
                    room_category_id = Room_category.objects.get(id = id)
                    
            

                    message = {
                        'id': room_category_id.id,
                        'department_name': room_category_id.department_id,
                        'CategoryName': room_category_id.Category_name,
                        'Description': room_category_id.Discription,
                        
                    }
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


#---------room pagenation -----------------------------#
def add_room(request):
    try:
        if request.user.has_perm('APEN.   view_room'):
            room_category = Room_category.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            Room_list = []
            Status="availible"
            # total_beds = Beds.objects.all().count()
            # beds1 = Beds.objects.aggregate(Sum("id"))["id__sum"]

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                Room_list =Room.objects.filter(
                    Q(Room_NO__icontains = SearchQuery) |
                    Q(status__icontains = SearchQuery)

                )
            else:
                Room_list =Room.objects.all()

            paginator = Paginator(Room_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # room = Room.objects.get(Room_NO='123')  # Assuming '123' is the room number of the desired room
            # occupied_beds = Beds.objects.filter(Room=room, status='occupied').count()
            # total_beds = Beds.objects.filter(Room=room).count()
            # available_beds = total_beds - occupied_beds

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Room category List',
                'room_category' : room_category,
                'Status':Status ,
                # 'total_beds': total_beds
            }
            return render(request, 'Rooms_and_beds/add_room.html',context)
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

#----------add room ------------------#
def manage_room(request,action):
    try:
        if request.user.has_perm('APEN.add_room'):
            if action == 'new_room':
            
                if request.method == 'POST':
                    # Get all data from the request
                    RoomCtategory = request.POST.get('RoomCtategory')
                    RoomNo = request.POST.get('RoomNo')
                
                    # Validaet dat
                    if RoomCtategory == '' or RoomCtategory == 'null' or RoomCtategory is None or RoomCtategory == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select room category ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if RoomNo == '' or RoomNo == 'null' or RoomNo is None or RoomNo == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter category name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                RoomCtategory = RemoveSpecialCharacters(RoomCtategory)
                RoomNo = RemoveSpecialCharacters(RoomNo)
                # depatment_id = Departments.objects.get(id=CategoryName)
                status1 = 'availible'
                new_room = Room(Room_category_id=RoomCtategory , Room_NO = RoomNo,status=status1)
                new_room.save()

                return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'new Room has been created',
                                'title': 'masha allah !',
                                'type': 'success+',
                            }
                        )
        else:
                return render(request, 'Hr/403.html')
        if request.user.has_perm('APEN.    change_room'):
            if action == 'update_room':
                        if request.method == 'POST':
                        # Get all data from the request
                            id = request.POST.get('id')
                            RoomCtategory = request.POST.get('RoomCtategory')
                            RoomNo = request.POST.get('RoomNo')
                            
                                
                            # Validaet data
                            if RoomCtategory == '' or RoomCtategory == 'null' or RoomCtategory is None or RoomCtategory == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter RoomCtategory ',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            if RoomNo == '' or RoomNo == 'null' or RoomNo is None or RoomNo == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter RoomNo',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )

                            

                            room_cat = Room_category.objects.get(id=RoomCtategory)
                            update_room= Room.objects.get(id=id)
                            update_room.Room_category = room_cat
                            update_room.Room_NO = RoomNo 
                        
                            
                            update_room.save()
                            return JsonResponse(
                                {
                                        'isError': False,
                                        'Message': 'an Room  Category has been updated',
                                        'title': 'masha allah !' + RoomNo + " been updated" ,
                                        'type': 'success',
                                    }
                                )
        else:
                return render(request, 'Hr/403.html')
                

        if action == "getroom":
                if request.method == 'POST':
                    id = request.POST.get('id')
                
                    room_id = Room.objects.get(id = id)
                    message = {
                        'id': room_id.id,
                        'RoomCtategory': room_id.Room_category_id,
                        'RoomNo': room_id.Room_NO,
                        
                        
                    }
                return JsonResponse({'isError': False, 'Message': message}, status=200)
        
        if action == "add_bed":
            
            if request.method == 'POST':
                id = request.POST.get('id')
            
                room_id = Room.objects.get(id=id)
                message = {
                    'id': room_id.id,
                    
                    'RoomNomber': room_id.Room_NO,
        
                }
            return JsonResponse({'isError': False, 'Message': message}, status=200)
        if action == 'new_bed':
                if request.method == 'POST':
                # Get all data from the request
                    
                    roomno = request.POST.get('roomno')
                    RoomNomber = request.POST.get('RoomNomber')
                    BedNo = request.POST.get('BedNo')
                    
                    
                        
                    # Validaet data
                    if RoomNomber == '' or RoomNomber == 'null' or RoomNomber is None or RoomNomber == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter RoomNomber',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if BedNo == '' or BedNo == 'null' or BedNo is None or BedNo == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter BedNo',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        ) 
                Status = "Available"
                
                
                get_roomno= Room.objects.get(id=roomno)
                new_bed = Beds(Room_id=get_roomno.id,BedNO=BedNo,status=Status)
                new_bed.save()

                return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'medicine  cat has been updated',
                                'title': 'mohamed !' + BedNo + " been updated" ,
                                'type': 'success',
                            }
                        )
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

def room_view(request,pk):
    room =Room.objects.get(id=pk)
    Bed = Beds.objects.filter(Room=room.id)
    total_beds = Beds.objects.all().count()
    paitient=AssignBed.objects.filter(Room=room.id)

    for p in paitient:
         print(p.Admission)


    context = {
        'room' : room,
        'id': pk,
        'bed': Bed,
        'total_beds':total_beds,
        'paitient':paitient
    }
    return render(request, 'Rooms_and_beds/view_room_details.html',context) 
#----------------Beds---------------------------#
def add_bed(request):
    try:
        if request.user.has_perm('APEN.view_beds'):
            room = Room.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            Room_list = []
            Status="availible"

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                Room_list =Beds.objects.filter(
                    Q(BedNO__icontains = SearchQuery) |
                    Q(status__icontains = SearchQuery)|
                    Q(Room__Room_NO__icontains =SearchQuery)

                )
            else:
                Room_list =Beds.objects.all()

            paginator = Paginator(Room_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Room category List',
                'room' : room,
                'Status':Status 
            }
            return render(request, 'Rooms_and_beds/add_bed.html',context)
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


def manage_bed(request,action):
    try:
        if request.user.has_perm('APEN.add_beds'):
            if action == 'new_bed':
            
                if request.method == 'POST':
                    # Get all data from the request
                    RoomNomber = request.POST.get('RoomNomber')
                    bed_no = request.POST.get('bed_no')
                
                    # Validaet dat
                    if RoomNomber == '' or RoomNomber == 'null' or RoomNomber is None or RoomNomber == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select room no ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if bed_no == '' or bed_no == 'null' or bed_no is None or bed_no == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter bed_no',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                
                
                status1 = 'Empty'
                new_bed = Beds(Room_id=RoomNomber , BedNO = bed_no,status=status1)
                new_bed.save()

                return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'new Bed has been created',
                                'title': 'masha allah !',
                                'type': 'success+',
                            }
                        )
        else:
                return render(request, 'Hr/403.html')
        

        if action == "getbed":
                if request.method == 'POST':
                    id = request.POST.get('id')
                
                    bed_id = Beds.objects.get(id = id)
                    message = {
                        'id': bed_id.id,
                        'RoomNomber': bed_id.Room_id,
                        'bed_no': bed_id.BedNO,
                        
                        
                    }
                return JsonResponse({'isError': False, 'Message': message}, status=200)
        if request.user.has_perm('APEN. change_beds'):
            if action == 'update_bed':
                        if request.method == 'POST':
                        # Get all data from the request
                            id = request.POST.get('id')
                            RoomNomber = request.POST.get('RoomNomber')
                            bed_no = request.POST.get('bed_no')
                            
                                
                            # Validaet data
                            if RoomNomber == '' or RoomNomber == 'null' or RoomNomber is None or RoomNomber == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter RoomNomber ',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            if bed_no == '' or bed_no == 'null' or bed_no is None or bed_no == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter bed_no',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )

                            
                            RoomNomber = RemoveSpecialCharacters(RoomNomber)
                            bed_no = RemoveSpecialCharacters(bed_no)
                            room = Room.objects.get(id=RoomNomber)
                            update_bed= Beds.objects.get(id=id)
                            update_bed.Room = room
                            update_bed.BedNO = bed_no
                        
                            
                            update_bed.save()
                            return JsonResponse(
                                {
                                        'isError': False,
                                        'Message': 'an Bed has been updated',
                                        'title': 'masha allah !' + bed_no + " been updated" ,
                                        'type': 'success',
                                    }
                                )
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
                



            