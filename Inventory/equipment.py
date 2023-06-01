from django.shortcuts import render , redirect

from Users.models import sendException
from .models import Medicine ,Medicine_categories , Equipment_categories , Equipment , MedicineTransection , EquipmentTransection, lost_and_dameged_equipment
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from LRPD.models import MedicineOrder , MedicineOrderDetails ,LabEquipmentOrder, pharmacy_medicine ,PharmacyTransection
from django.contrib.auth.decorators import login_required
import re
from Hr.views import RemoveSpecialCharacters, text_validation, text_validationNumber,  number_validation, phone_valid, check
from  .views import *

#----------------- equoment cat pagenition -----------
@login_required(login_url='Login')
def equipment_categories(request):
        
    try:
        if request.user.has_perm('Inventory.  view_equipment_categories'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            store_category_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                store_category_list =Equipment_categories.objects.filter(
                    Q(category_name__icontains = SearchQuery) 
                
                    
                )
            else:
                store_category_list =Equipment_categories.objects.all()

            paginator = Paginator(store_category_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'store category List'


            }
            return render (request, 'equipment/Equipment_catigory.html',context)
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

#----------------new_equipment_category-----------------
@login_required(login_url='Login')
def manage_equipment_cat(request, action):
     try:
        if request.user.has_perm('Inventory.  add_equipment_categories'):
            if action == 'new_equipment_category':
                if request.method == 'POST':
                    # Get all data from the request
                    Category_Name = request.POST.get('Category_Name')
                    Description = request.POST.get('Description')
                    # Validaet data
                    if Category_Name == '' or Category_Name == 'null' or Category_Name is None or Category_Name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter category name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Category_Name) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for Category_Name name',
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
                    if text_validation(Description) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for Description ',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                Category_Name = RemoveSpecialCharacters(Category_Name)
                Description = RemoveSpecialCharacters(Description)
                    
        
                
                add_store_category = Equipment_categories(category_name = Category_Name, discription= Description)
                add_store_category.save()
            
                return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'new store_cat has been created',
                                'title': 'masha allah !',
                                'type': 'success+',
                            }
                        ) 
        else:
            return render(request, 'Hr/403.html')
        if request.user.has_perm('Inventory.  change_equipment_categories'):
            if action == 'update_equipmen_category':
                if request.method == 'POST':
                # Get all data from the request
                    equipment_category_id = request.POST.get('CategoryID')
                    Category_Name = request.POST.get('Category_Name')
                    Description = request.POST.get('Description')
                        
                    # Validaet data
                    if Category_Name == '' or Category_Name == 'null' or Category_Name is None or Category_Name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter first name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Category_Name) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for Category_Name name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                    if Description == '' or Description == 'null' or Description is None or Description == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Descriptionme',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Description) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for Description name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                    
                    update_equipment_category= Equipment_categories.objects.get(id=equipment_category_id)
                    update_equipment_category.category_name = Category_Name
                    update_equipment_category.discription = Description
                    
                    update_equipment_category.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'Equipment cat has been updated',
                                'title': 'mohamed !' + Category_Name + " been updated" ,
                                'type': 'success',
                            }
                        )    
        else:
            return render(request, 'Hr/403.html')
        if action == "getequipmentcat":
            if request.method == 'POST':
                id = request.POST.get('category_id')
            
                category_id = Equipment_categories.objects.get(id = id)
                
        

                message = {
                    'id': category_id.id,
                    'category_name': category_id.category_name,
                    'Description': category_id.discription,
                    
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
     #end except 

#---delete equipmentcat----
@login_required(login_url='Login')
def delete_equipment_category(request,delete_equipment_category_id):
    if request.user.has_perm('Inventory.  delete_equipment_categories'):
        store_category1 = Equipment_categories.objects.get(pk=delete_equipment_category_id)
        store_category1.delete()
        return redirect('equipment_categories')
    else:
            return render(request, 'Hr/403.html')


#-------equipment paginion---------
@login_required(login_url='Login')
def equipment(request):
     try:
        if request.user.has_perm('Inventory.  view_equipment'):
            store_category = Equipment_categories.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            equipment_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']

                equipment_list =Equipment.objects.filter(
                    Q(item_name__icontains = SearchQuery) 
                    
                )
            else:
                equipment_list =Equipment.objects.all()

            paginator = Paginator(equipment_list, DataNumber)
            print(paginator)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'store List',
                'Equipment_categories': store_category


            }
            return render (request, 'equipment/Equipment.html',context)
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



#-----new equipment ----------
@login_required(login_url='Login')
def manage_equipment(request,action):
    # try:      
    # This action will create a new account
        if request.user.has_perm('Inventory.  add_equipment'):
            if action == 'new_equipment':
                if request.method == 'POST':
                    # Get all data from the request
                    ItemName = request.POST.get('ItemName')
                    select_store_cat = request.POST.get('select_store_cat')
                    quantity = request.POST.get('quantity')
                    Lost_and_damage = request.POST.get('Lost_and_damage')
                    manufaturing = request.POST.get('manufaturing')
                    supplier_price = request.POST.get('supplier_price')
                    
                    select_employe = request.POST.get('select_employe')
                

                    # Validaet data
                    if ItemName == '' or ItemName == 'null' or ItemName is None or ItemName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter item name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(ItemName) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for ItemName name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                    if select_store_cat == '' or select_store_cat == 'null' or select_store_cat is None or select_store_cat == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter select cat',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    

                    if quantity == '' or quantity == 'null' or quantity is None or quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter qrt ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Lost_and_damage == '' or Lost_and_damage == 'null' or Lost_and_damage is None or Lost_and_damage == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter lost and damage',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if manufaturing == '' or manufaturing == 'null' or manufaturing is None or manufaturing == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select manufaturing',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(manufaturing) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only for manufaturing name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                    if supplier_price == '' or supplier_price == 'null' or supplier_price is None or supplier_price == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Please select supplier price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                ItemName  = RemoveSpecialCharacters(ItemName)
                select_store_cat =RemoveSpecialCharacters(select_store_cat)
                quantity = RemoveSpecialCharacters(quantity)
                Lost_and_damage=RemoveSpecialCharacters(Lost_and_damage)
                manufaturing = RemoveSpecialCharacters(manufaturing)
                supplier_price =RemoveSpecialCharacters(supplier_price)
                
                status = "Available"
                Type =  "purchase"
                tno= "P001"

                qty_equipment = int(quantity)-int(Lost_and_damage)
                add_store = Equipment(item_name = ItemName, category_id= select_store_cat, quantity=qty_equipment, lost_and_damaged = Lost_and_damage, manufacturing= manufaturing, supplier_price=supplier_price)
                add_store.save()

                reson="Equipment damaeged"
                status1="damaged"
                equipmentid = Equipment.objects.get(id=add_store.id)
                new_lost_and_damaged =lost_and_dameged_equipment(Equipment_name_id=equipmentid.id,lost_and_damaged=Lost_and_damage,reason=reson,Status=status1)
                new_lost_and_damaged.save()

                equipment_transection = EquipmentTransection(EqId=equipmentid,Type=Type,quantity=qty_equipment, lost_and_damaged=Lost_and_damage,manufacturing=manufaturing,supplier_price= supplier_price,Transectno=tno,status=status )
                equipment_transection.save()


                return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new store has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            )
        
        
        
            if action == 'new_refill_equipment':
                if request.method == 'POST':
                    # Get all data from the request
                    EquipmentID = request.POST.get('EquipmentID')
                    EquipmenCat = request.POST.get('EquipmenCat')
                    SelectStoreCat = request.POST.get('SelectStoreCat')
                    Lost_and_damage2 = request.POST.get('Lost_and_damage2')
                    quantity2 = request.POST.get('quantity2')
                    manufaturing2 = request.POST.get('manufaturing2')
                    supplier_price2 = request.POST.get('supplier_price2')
                    
                    
                

                    # Validaet data
                    if EquipmenCat == '' or EquipmenCat == 'null' or EquipmenCat is None or EquipmenCat == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter item name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    # if text_validation(ItemName) == False:
                    #         return JsonResponse(
                    #             {
                    #                 'isError': True,
                    #                 'Message': 'Please enter text only for ItemName name',
                    #                 'title': 'Validation Error!',
                    #                 'type': 'warning',
                    #             }
                    #         )

                    if SelectStoreCat == '' or SelectStoreCat == 'null' or SelectStoreCat is None or SelectStoreCat == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter select cat',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    

                    if quantity2 == '' or quantity2 == 'null' or quantity2 is None or quantity2 == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter qrt ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Lost_and_damage2 == '' or Lost_and_damage2 == 'null' or Lost_and_damage2 is None or Lost_and_damage2 == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter lost and damage',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if manufaturing2 == '' or manufaturing2 == 'null' or manufaturing2 is None or manufaturing2 == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select manufaturing',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if supplier_price2 == '' or supplier_price2 == 'null' or supplier_price2 is None or supplier_price2 == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Please select supplier price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                status = "Available"
                Type =  "Refill"
                tno= "PR002"
                qty_eq_rifill = int(quantity2)-int(Lost_and_damage2)
                get_equipment = Equipment.objects.get(id=EquipmentID)
                equipment_qty = get_equipment.quantity
                new_equipment_qty = int(equipment_qty) + int(quantity2) -int(Lost_and_damage2)
                
                get_equipment.quantity = new_equipment_qty
                get_equipment.save()


                reson="Refil Equipment damaeged"
                status1="damaged"
                
                new_lost_and_damaged =lost_and_dameged_equipment(Equipment_name_id=get_equipment.id,lost_and_damaged=Lost_and_damage2,reason=reson,Status=status1)
                new_lost_and_damaged.save()

                equipment_transection = EquipmentTransection(EqId=get_equipment,Type=Type,quantity=qty_eq_rifill, lost_and_damaged=Lost_and_damage2,manufacturing=manufaturing2,supplier_price= supplier_price2,Transectno=tno,status=status )
                equipment_transection.save()


                return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new Equipment has refiiled',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            )
        else:
            return render(request, 'Hr/403.html')
        
        if request.user.has_perm('Inventory.  change_equipment'):
        #------------UPDATE EQUIPMENT -----------------
            if action == 'update_equipment':
                if request.method == 'POST':
                # Get all data from the request
                    EquipmentID = request.POST.get('EquipmentID')
                    ItemName = request.POST.get('ItemName')
                    select_store_cat = request.POST.get('SelectCategory')
                    quantity = request.POST.get('quantity')
                    Lost_and_damage = request.POST.get('Lost_and_damage')
                    
                    manufaturing = request.POST.get('manufaturing')
                    supplier_price = request.POST.get('supplier_price')
                    select_employe = request.POST.get('select_employe')
                    
                    # Validaet data
                    

                    
                    update_equipment= Equipment.objects.get(id=EquipmentID)
                    update_equipment.item_name = ItemName
                    update_equipment.select_store_cat = select_store_cat
                    update_equipment.quantity = quantity
                    update_equipment.lost_and_damaged = Lost_and_damage
                    update_equipment.manufacturing = manufaturing
                    update_equipment.supplier_price = supplier_price
                    
                    
                    update_equipment.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'Medicine has been updated',
                                'title': 'masha allah !' + ItemName + " been updated" ,
                                'type': 'success',
                            }
                        )
        else:
            return render(request, 'Hr/403.html')
        #-----------REED EQUIPMENT --------------
        if action == "getEquipment":
            if request.method == 'POST':
                id = request.POST.get('EquipmentID')
            
                Equipment_id = Equipment.objects.get(id=id)
                
        

                message = {
                    'id': Equipment_id.id,
                    'ItemName': Equipment_id.item_name,
                    'select_store_cat': Equipment_id.category_id,
                    'quantity': Equipment_id.quantity,
                    'Lost_and_damage': Equipment_id.lost_and_damaged,
                    'manufaturing': Equipment_id.manufacturing,
                    
                    'supplier_price': Equipment_id.supplier_price,
                    
                    
                }
        
        if action == "refillEquipment":
         
         if request.method == 'POST':
            id = request.POST.get('Equipment_id')
        
            equipment_id = Equipment.objects.get(id=id)
            
    

            message = {
                'id': equipment_id.id,
                
                'EquipmenCat': equipment_id.item_name,
                'SelectStoreCat': equipment_id.category.category_name,
                
                
                
            }
        return JsonResponse({'isError': False, 'Message': message}, status=200)
    
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
        



#--------delete equipement --------------
@login_required(login_url='Login')
def delete_equipment(request,Equipment_id):
    if request.user.has_perm('Inventory.   delete_equipment'):
        delete_equipment = Equipment.objects.get(pk=Equipment_id)
        delete_equipment.delete()
        return redirect('equioment')
    else:
            return render(request, 'Hr/403.html')
    


#-------------EQUIPMENT PAGE order-----------
@login_required(login_url='Login')
def equipment_order(request):
     try:
        if request.user.has_perm('Inventory. add_equipment'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =LabEquipmentOrder.objects.filter(
                    Q(Order_Date__icontains = SearchQuery) |
                    Q(Status__icontains = SearchQuery) |
                    Q(Item__item_name__icontains = SearchQuery) 
                    
                )
            else:
                order =LabEquipmentOrder.objects.all().order_by(
                    Case(
                        When(Status="Pending" , then=1),
                        When(Status="Approved",then=2)
                       
                    )
               
                )

            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Status = 'Approved'
            totalorder = MedicineOrder.objects.all()
            total=len(totalorder)
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                'status' : Status,
                'total_pages':total 
            }
            return render (request, 'equipment/GetEquipmentOrder.html',context)
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



#--------------manage equipment order------------
@login_required(login_url='Login')
def manage_order_equipment(request, action):
    try:
        if request.user.has_perm('Inventory. add_equipment'):
          

            if action == "get_approveEquipment":
                if request.method == 'POST':
                    id = request.POST.get('OrderId')
                    
                
                    order_id= LabEquipmentOrder.objects.get(id=id)
                    message = {
                        'id': order_id.id,
                        'Status':order_id.Status
                        
                    }
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            
            if action == "approveEquipment":
                if request.method == 'POST':
                    id = request.POST.get('OrderId')
                    
                    Status = "Approved" 
                    status = "Approved" 
                
                    Type = "paid"
                    # tno= "P002"
                    order_approve1= LabEquipmentOrder.objects.get(id=id)
                    order_approve3= order_approve1.Quantity
                    order_approve2= order_approve1.Item.quantity
                    totally_approve= order_approve2 - order_approve3
                    item = Equipment.objects.get(id=order_approve1.Item.id)
                    
                    item.quantity = totally_approve
                    item.save()
                    order_approve1.Status = Status
                    order_approve1.save()
                    # transectio_equipment = Equipment.objects.get(id=item.id)

                    paid_equipment = EquipmentTransection(EqId_id=item.id,Type=Type,quantity=order_approve3,lost_and_damaged=item.lost_and_damaged,manufacturing=item.manufacturing,supplier_price=item.supplier_price,Transectno=GenerateSerialNumber(),status=status)
                    paid_equipment.save()

                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'Your request approved',
                                'title': "ok ! b" ,
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


def view_equipment(request,pk):
    if request.user.has_perm('Inventory.  view_equipment'):

        equipment_view =Equipment.objects.get(id=pk)
        transection_equipment = EquipmentTransection.objects.filter(EqId=pk)

        context = {
            'equipment' : equipment_view,
            'id': pk,
            'transections': transection_equipment

        }

        return render(request, 'equipment/view_equipment_details.html',context) 
    else:
            return render(request, 'Hr/403.html')

@login_required(login_url='Login')
def Lost_and_damed(request):
    # try:
        if request.user.has_perm('Inventory.view_equipment'):
            store_category1 = Equipment_categories.objects.all()
            Equipment1 = Equipment.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            order = []
        
            Status1 = 'damaged'
            Type = 'purchase'
            # today = date.today()

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                order =lost_and_dameged_equipment.objects.filter(Status=Status1
                    #  Q(lost_and_damaged__icontains = SearchQuery)
                
                    
                )
            else:
                order =lost_and_dameged_equipment.objects.filter(Status=Status1)
                
            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                
                'Status1': Status1,
                'store_category1':  store_category1,
                'Equipment1':Equipment1

                # 'expired':Expaire_medicine_list
            }
            return render(request, 'equipment/lost_and_dameged.html',context)  
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

def manage_lost_and_damage_equipment(request,action):
        # try:
            # if request.user.has_perm('Inventory.add_medicine_categories'):
   
                if action == 'lost_and_damaged_equipment':
                    if request.method == 'POST':
                        # Get all data from the request
                       
                        Equipment1 = request.POST.get('Equipment')
                        Quentity = request.POST.get('Quentity')
                        Reason = request.POST.get('Reason')
                       


                    
                        # Validaet data
                        if Equipment1 == '' or Equipment1 == 'null' or Equipment1 is None or Equipment1 == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter equipment name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                        if Quentity == '' or Quentity == 'null' or Quentity is None or Quentity == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter discription ',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if Reason == '' or Reason == 'null' or Reason is None or Reason == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter discription ',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                   
                    Reason = RemoveSpecialCharacters(Reason)
                    status="damaged"
                   

                    add_lost_and_damaged_equipment = lost_and_dameged_equipment(Equipment_name_id=Equipment1, lost_and_damaged= Quentity,reason=Reason,Status=status)
                   
                    add_lost_and_damaged_equipment.save()
                    quentity1 = Equipment.objects.get(id=Equipment1)
                    equ_qty=quentity1.quantity

                    lost=int(equ_qty)-int(Quentity)
                    quentity1.quantity=lost
                    # print(quentity1.id)
                    # print(equ_qty)
                    # print(lost)

                    quentity1.save()
                    
                
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new Lost and damage has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                

