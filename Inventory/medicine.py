from collections import Counter
from django.shortcuts import render , redirect
from Hr.views import RemoveSpecialCharacters

from Users.models import sendException
from .models import Medicine ,Medicine_categories , Equipment_categories , Equipment , MedicineTransection
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from LRPD.models import MedicineOrder , MedicineOrderDetails ,LabEquipmentOrder, pharmacy_medicine ,PharmacyTransection
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
@login_required(login_url='Login')
def Medicine_category(request):
        try:
            if request.user.has_perm('Inventory.view_medicine_categories'):
                CheckSearchQuery = 'SearchQuery' in request.GET
                CheckDataNumber = 'DataNumber' in request.GET
                DataNumber = 10
                SearchQuery = ''
                Medicine_category_list = []

                if CheckDataNumber:
                    DataNumber = int(request.GET['DataNumber'])

                if CheckSearchQuery:
                    SearchQuery = request.GET['SearchQuery']
                    Medicine_category_list =Medicine_categories.objects.filter(
                        Q(medicine_cat_name__icontains = SearchQuery)    
                    )
                else:
                    Medicine_category_list =Medicine_categories.objects.all()

                paginator = Paginator(Medicine_category_list, DataNumber)

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                context = {

                    'page_objects': page_obj,
                    'SearchQuery': SearchQuery,
                    'DataNumber': DataNumber,
                    'pageTitle': 'Medicine category List'
                }
                return render(request, 'medicines/medicine_category.html',context)
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

def manage_category(request,action):
        try:
            if request.user.has_perm('Inventory.add_medicine_categories'):
   
                if action == 'new_category':
                    if request.method == 'POST':
                        # Get all data from the request
                        CategoryName = request.POST.get('CategoryName')
                        Description = request.POST.get('Description')
                    
                        # Validaet data
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
                    CategoryName = RemoveSpecialCharacters(CategoryName)
                    Description = RemoveSpecialCharacters(Description)

                    add_category = Medicine_categories(medicine_cat_name = CategoryName, discription= Description)
                    add_category.save()
                
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new medicicne category has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                if request.user.has_perm('Inventory. change_medicine_categories'):
                    if action == 'update_category':
                        if request.method == 'POST':
                        # Get all data from the request
                            Medicine_categories_id = request.POST.get('CategoryID')
                            CategoryName = request.POST.get('CategoryName')
                            Description = request.POST.get('Description')
                                
                            # Validaet data
                            if CategoryName == '' or CategoryName == 'null' or CategoryName is None or CategoryName == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter first name',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )

                            if Description == '' or Description == 'null' or Description is None or Description == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter father name',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            CategoryName = RemoveSpecialCharacters(CategoryName)
                            Description = RemoveSpecialCharacters(Description)
                

                            
                            update_category= Medicine_categories.objects.get(id=Medicine_categories_id)
                            update_category.medicine_cat_name = CategoryName
                            update_category.discription = Description
                            
                            update_category.save()
                            return JsonResponse(
                                {
                                        'isError': False,
                                        'Message': 'Medicine has been updated',
                                        'title': 'masha allah !' + CategoryName + " been updated" ,
                                        'type': 'success',
                                    }
                                )
                else:
                    return render(request, 'Hr/403.html')
                        
                if action == "getMedicineeCategories":
                    if request.method == 'POST':
                        id = request.POST.get('category_id')
                    
                        category_id = Medicine_categories.objects.get(id = id)
                        
                

                        message = {
                            'id': category_id.id,
                            'CategoryName': category_id.medicine_cat_name,
                            'Description': category_id.discription,
                            
                        }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
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
        
@login_required(login_url='Login')   
def delete_category(request,Medicine_categories_id):
        if request.user.has_perm('Inventory.  delete_medicine_categories'):
   
            medicine_category1 = Medicine_categories.objects.get(pk=Medicine_categories_id)
            medicine_category1.delete()
            return redirect('Medicine_category')
        else:
            return render(request, 'Hr/403.html')
    



#---------medicine pagenition----------
@login_required(login_url='Login')
def MedicineList(request):
    try:
        if request.user.has_perm('Inventory.   view_medicine'):
            medicine_category = Medicine_categories.objects.all()
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            MedicineList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                MedicineList =Medicine.objects.filter(
                    Q(Medicine_categories__medicine_cat_name__icontains = SearchQuery) |
                    Q(Medicine_name__icontains = SearchQuery) |
                    Q(status__icontains = SearchQuery) |
                     Q(manufacturing__icontains = SearchQuery) 
                    # Q(bach_no__icontains = SearchQuery)
                    
                )
            else:
                MedicineList =Medicine.objects.all()

            paginator = Paginator(MedicineList, DataNumber)
            status = 'Available'
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Medicine List',
                'status': status,
                'medicine_category':medicine_category}

            return render (request, 'medicines/Medicine.html',context)
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

#-----------------new medicine and refill ------------------
@login_required(login_url='Login')
def manage_medicine(request,action):
    # try: 
        if request.user.has_perm('Inventory.add_medicine'):
    
            if action == 'new_medicine':
                if request.method == 'POST':
                    # Get all data from the request
                    bach_no = request.POST.get('bach_no')
                    Medicine_name = request.POST.get('MedicineName')
                    Select_category = request.POST.get('SelectCategory')
                    box = request.POST.get('box')
                    quantity = request.POST.get('quantity')
                    dosage = request.POST.get('dosage')
                    manufacturing = request.POST.get('manufacturing')
                    manufacturingdate = request.POST.get('manufacturingdate')
                    
                    Expiry_date = request.POST.get('ExpireDate')
                    
                    
                    supplier_price = request.POST.get('supplierPrice')

                    
                    if bach_no == '' or bach_no == 'null' or bach_no is None or bach_no == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter bach_no',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Medicine_name == '' or Medicine_name == 'null' or Medicine_name is None or Medicine_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Medicine_name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Select_category == '' or Select_category == 'null' or Select_category is None or Select_category == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Select_category',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if box == '' or box == 'null' or box is None or box == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter box',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if quantity == '' or quantity == 'null' or quantity is None or quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter quantity',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if dosage == '' or dosage == 'null' or dosage is None or dosage == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter dosage',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if manufacturing == '' or manufacturing == 'null' or manufacturing is None or manufacturing == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an manufacturing',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if manufacturingdate == '' or manufacturingdate == 'null' or manufacturingdate is None or manufacturingdate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an manufacturing date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if Expiry_date == '' or Expiry_date == 'null' or Expiry_date is None or Expiry_date == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Enter Expiry_date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    
                    if supplier_price == '' or supplier_price == 'null' or supplier_price is None or supplier_price == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an supplier_price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                Medicine_name = RemoveSpecialCharacters(Medicine_name)
                Select_category=RemoveSpecialCharacters(Select_category)
                box = RemoveSpecialCharacters(box)
                quantity =RemoveSpecialCharacters(quantity)
                dosage =RemoveSpecialCharacters(dosage)
                manufacturing =RemoveSpecialCharacters(manufacturing)
                
                supplier_price = RemoveSpecialCharacters(supplier_price)




                status = "Available"
                Type =  "purchase"
                batch_no = Medicine_name[:4] + '0001'
            
                add_medicine = Medicine( Medicine_name = Medicine_name, Medicine_categories_id= Select_category, box=box,quantity=quantity,dosage=dosage,supplier_price=supplier_price, manufacturing = manufacturing,status=status)
                add_medicine.save()
                # today = datetime.datetime.now()
                # order =MedicineTransection.objects.filter(Expire_date__lte = today
                
                
                # ).order_by('Expire_date') 

                medid = Medicine.objects.get(pk=add_medicine.id)
                medtransaction = MedicineTransection(MedId =medid,Type=Type,box=box,qty=quantity ,BatchNO=batch_no,manufacturing_date =manufacturingdate,Expire_date =Expiry_date,supplier_price=supplier_price,status=status )  
                medtransaction.save()

                # expired1 = medtransaction.Expire_date = today
                # ex_box = medtransaction.box 
                
                # expired1.box - ex_box 

                return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new medicine has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            )
            if action == 'edit_refill_med_transaction':
                if request.method == 'POST':
                    # Get all data from the request
                    bach_no = request.POST.get('bach_no3')
                    box3 = request.POST.get('box3')
                    quantity = request.POST.get('quantity3')
                    dosage = request.POST.get('dosage')
                    manufacturingdate = request.POST.get('manufacturingdate3')
                    Expiry_date = request.POST.get('ExpireDate3')
                    
                    supplier_price = request.POST.get('supplierPrice3')
                    medicinerefilid = request.POST.get('Medicinerefilid')

                    
                    if bach_no == '' or bach_no == 'null' or bach_no is None or bach_no == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter bach_no',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    

                    if box3 == '' or box3 == 'null' or box3 is None or box3 == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter box',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if quantity == '' or quantity == 'null' or quantity is None or quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter quantity',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                   

                    
                    if manufacturingdate == '' or manufacturingdate == 'null' or manufacturingdate is None or manufacturingdate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an manufacturing date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if Expiry_date == '' or Expiry_date == 'null' or Expiry_date is None or Expiry_date == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Enter Expiry_date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    
                    if supplier_price == '' or supplier_price == 'null' or supplier_price is None or supplier_price == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an supplier_price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                status = "Available"
                
                Type =  "Refill"
               
                Med_id_transaction_refill=MedicineTransection.objects.get(id=medicinerefilid)
                old_medicine_refiled=Medicine.objects.get(id=Med_id_transaction_refill.MedId.id)

                refiled_box = Med_id_transaction_refill.box
                old_medicine_refiled_box = old_medicine_refiled.box
                new_box_refiled = (old_medicine_refiled_box - refiled_box)+int(box3)
                old_medicine_refiled.box=new_box_refiled
                old_medicine_refiled.save()



                Med_id_transaction_refill.BatchNO=bach_no
                Med_id_transaction_refill.box=int(box3)
                Med_id_transaction_refill.Expire_date=Expiry_date
                Med_id_transaction_refill.manufacturing_date=manufacturingdate
                Med_id_transaction_refill.supplier_price=supplier_price
                Med_id_transaction_refill.qty=quantity
                Med_id_transaction_refill.Type=Type
                Med_id_transaction_refill.save()


                # update_medicine_tranaction_refill = MedicineTransection( id=medid.id, box=box,qty=quantity,supplier_price=supplier_price, manufacturing_date = manufacturingdate,Type=Type,Expire_date=Expiry_date,status=status)
                # update_medicine_tranaction_refill.save()
                # today = datetime.datetime.now()
                # order =MedicineTransection.objects.filter(Expire_date__lte = today
                
                # ).order_by('Expire_date') 

                # medid = Medicine.objects.get(pk=add_medicine.id)
                # medtransaction = MedicineTransection(MedId =medid,Type=Type,box=box,qty=quantity ,BatchNO=bach_no,manufacturing_date =manufacturingdate,Expire_date =Expiry_date,supplier_price=supplier_price,status=status )  
                # medtransaction.save()

                return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new medicine has been updated',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            )
            

            if action == 'edit_purchase_medicine_transaction':
                if request.method == 'POST':
                    # Get all data from the request
                    bach_no = request.POST.get('bach_no2')
                    box2 = request.POST.get('box2')
                    quantity = request.POST.get('quantity2')
                   
                    manufacturingdate = request.POST.get('manufacturingdate2')
                    Expiry_date = request.POST.get('ExpireDate2')
                    
                    supplier_price = request.POST.get('supplierPrice2')
                    medicine_purchase_transaction = request.POST.get('medicineid')

                    
                    if bach_no == '' or bach_no == 'null' or bach_no is None or bach_no == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter bach_no',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    

                    if box2 == '' or box2 == 'null' or box2 is None or box2 == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter box',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if quantity == '' or quantity == 'null' or quantity is None or quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter quantity',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                   

                    
                    if manufacturingdate == '' or manufacturingdate == 'null' or manufacturingdate is None or manufacturingdate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an manufacturing date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if Expiry_date == '' or Expiry_date == 'null' or Expiry_date is None or Expiry_date == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Enter Expiry_date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    
                    if supplier_price == '' or supplier_price == 'null' or supplier_price is None or supplier_price == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an supplier_price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                status = "Available"
                
                Type =  "purchase"
               
                Med_id_transaction_purchase=MedicineTransection.objects.get(id=medicine_purchase_transaction)
                old_medicine=Medicine.objects.get(id=Med_id_transaction_purchase.MedId.id)

                purchase_box = Med_id_transaction_purchase.box
                old_medicine_box = old_medicine.box
                new_box = (old_medicine_box - purchase_box)+int(box2)
                old_medicine.box=new_box
                old_medicine.save()

                Med_id_transaction_purchase.BatchNO=bach_no
                Med_id_transaction_purchase.box=int(box2)
                Med_id_transaction_purchase.Expire_date=Expiry_date
                Med_id_transaction_purchase.manufacturing_date=manufacturingdate
                Med_id_transaction_purchase.supplier_price=supplier_price
                Med_id_transaction_purchase.qty=quantity
                Med_id_transaction_purchase.Type=Type


               

                # # if old_medicine.box == box2:
                # #     old_medicine.box=box

                # # elif:
                # #     old_medicine.box < box2
                # #     old_medicine.box+int(box2)
                # # else:
                # #     old_medicine.box > box2
                # #     old_medicine.box -int(box2)
                
                # if old_medicine.box == box2:
                #     old_medicine.box = box
                # elif old_medicine.box < box2:
                #     old_medicine.box + int(box2)
                # else:
                #     old_medicine.box - int(box2)


                
                Med_id_transaction_purchase.save()

                return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new medicine has been updated',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            )


        
            if action == 'new_refill':
                if request.method == 'POST':
                # Get all data from the request
                    
                    MedicineID = request.POST.get('medid')
                    Medicine_name = request.POST.get('MedicineName2')
                    Select_category = request.POST.get('SelectCategory2')
                    bach_no = request.POST.get('bach_no2')
                    box = request.POST.get('box2')
                    quantity = request.POST.get('quantity2')
                
                
                    manufacturingdate = request.POST.get('manufacturingdate2')
                    
                    Expire_date = request.POST.get('ExpireDate2')
                    
                    supplier_price = request.POST.get('supplierPrice2')
                        
                    # Validaet data
                    if bach_no == '' or bach_no == 'null' or bach_no is None or bach_no == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter bach_no',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Medicine_name == '' or Medicine_name == 'null' or Medicine_name is None or Medicine_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Medicine_name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Select_category == '' or Select_category == 'null' or Select_category is None or Select_category == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Select_category',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if box == '' or box == 'null' or box is None or box == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter box',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if quantity == '' or quantity == 'null' or quantity is None or quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter quantity',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    
                    if manufacturingdate == '' or manufacturingdate == 'null' or manufacturingdate is None or manufacturingdate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an manufacturing',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                
                    if Expire_date == '' or Expire_date == 'null' or Expire_date is None or Expire_date == 'undefined':
                            return JsonResponse(
                                {
                                'isError': True,
                                'Message': 'Enter Expiry_date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    
                    if supplier_price == '' or supplier_price == 'null' or supplier_price is None or supplier_price == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an supplier_price',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                # Medicine_name = RemoveSpecialCharacters(Medicine_name)
                # Select_category=RemoveSpecialCharacters(Select_category)
                # box = RemoveSpecialCharacters(box)
                # quantity =RemoveSpecialCharacters(quantity)
                # # dosage =RemoveSpecialCharacters(dosage)
                # manufacturing =RemoveSpecialCharacters(manufacturing)
                
                
                # supplier_price = RemoveSpecialCharacters(supplier_price)
                status = "Available"
                
                Type =  "Refill"
                get_medicine= Medicine.objects.get(id=MedicineID)
                medicine_box = get_medicine.box
                new_mediicne =  int(medicine_box) + int(box)
                get_medicine.box=new_mediicne
                get_medicine.save()
                
                refill_list = []
                med_transection = MedicineTransection.objects.filter(MedId = get_medicine.id)
                serial = 0
                for med_trans in med_transection:
                    if  med_trans.Type == "Refill":

                        serial = int(med_trans.BatchNO[4:])
                        serial = serial + 1

                        if serial < 10:
                            serial = '000' + str(serial)
                        elif serial < 100:
                            serial = '00' + str(serial)
                        elif serial < 1000:
                            serial = '0' + str(serial)
                    elif med_trans.Type == "purchase":

                        serial = int(med_trans.BatchNO[4:])
                        serial = serial + 1

                        if serial < 10:
                            serial = '000' + str(serial)
                        elif serial < 100:
                            serial = '00' + str(serial)
                        elif serial < 1000:
                            serial = '0' + str(serial)
                batch_num = get_medicine.Medicine_name[:4]+str(serial)
            
                
                

                
                medtransaction = MedicineTransection(MedId_id=get_medicine.id,Type=Type,box=box,qty=quantity ,BatchNO=batch_num,manufacturing_date=manufacturingdate,Expire_date =Expire_date,supplier_price=supplier_price,status=status )  
                medtransaction.save()

                return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'medicine  has been Refiiled ',
                                'title': 'mohamed !' + Medicine_name + " been updated" ,
                                'type': 'success',
                            }
                        )
        else:
            return render(request, 'Hr/403.html') 
        
        if request.user.has_perm('Inventory.change_medicine'):
            if action == 'update_medicine':
                if request.method == 'POST':
                # Get all data from the request
                    
                    MedicineID = request.POST.get('MedicineID1')
                    Medicine_name = request.POST.get('MedicineName')
                    Select_category = request.POST.get('SelectCategory')
                   
                    

                    
                    getmedicinecat = Medicine_categories.objects.get(id=Select_category)
                    # status = "Available"
                    # print(MedicineID)
                    update_medicine= Medicine.objects.get(id=MedicineID)
                    # update_transsection = MedicineTransection.objects.get(MedId=update_medicine.id)
                    
                    update_medicine.Medicine_name = Medicine_name
                    update_medicine.Medicine_categories = getmedicinecat 
                   
                    
                    update_medicine.save()
                    # update_transsection.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'medicine   has been updated',
                                'title': 'mohamed !' + Medicine_name + " been updated" ,
                                'type': 'success',
                            }
                        )
        else:
            return render(request, 'Hr/403.html') 

        if action == "getMedicine":
            if request.method == 'POST':
                id = request.POST.get('Medicine_id')
            
                medicine_id = Medicine.objects.get(id=id)
                # transsection = MedicineTransection.objects.get(MedId=medicine_id.id)
                
        

                message = {
                    'id': medicine_id.id,
                    
                    
                    'MedicineName': medicine_id.Medicine_name,
                    'SelectCategory': medicine_id.Medicine_categories_id,
                    # 'BatchNO': transsection.BatchNO,
                    # 'box': medicine_id.box,
                    # 'quantity': medicine_id.quantity,       
                    # 'dosage': medicine_id.dosage,
                    # 'manufacturing': medicine_id.manufacturing,
                    # 'manufacturing_date': transsection.manufacturing_date,
                    
                    # 'Expire_date': transsection.Expire_date,
                    
                    
                    # 'supplierPrice': medicine_id.supplier_price,
                    
                }
            return JsonResponse({'isError': False, 'Message': message}, status=200) 
        
        
        
        
        if action == "refill":
         
         if request.method == 'POST':
            
            id = request.POST.get('Medicine_id')
        
            medicine_id = Medicine.objects.get(id=id)
            
    

            message = {
                'id': medicine_id.id,
                
                'MedicineName1': medicine_id.Medicine_name,
                'SelectCategory1': medicine_id.Medicine_categories.medicine_cat_name,
                
                
                
            }
        


        if action == "i_inventory":
            year = request.POST.get('yearr')
            today = date.today()
            
            MedicineList =Medicine.objects.filter(
                Q(status__icontains = 'Available')   
            ).count()
             
            MedicineListpaid =MedicineTransection.objects.filter(
                Q(Type__icontains = 'paid')   
            ).count()
            



            ExpireMedicine=MedicineTransection.objects.filter(Expire_date__lte = today).count()
            
            message = {
                    'MedicineListpaid': MedicineListpaid,
                    'mediicne_list': MedicineList,
                    'ExpireMedicine': ExpireMedicine
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

def view_medicine(request, pk):
    try:
        if request.user.has_perm('Inventory.view_medicine'):
            
            medicine_view = Medicine.objects.get(id=pk)
            medicines = MedicineTransection.objects.all()
            transection_medicine_view = MedicineTransection.objects.filter(MedId=pk)

            context = {'medicine': medicine_view,
                    'id':pk,
                    'transection' : transection_medicine_view,
                    'medicines'  :  medicines
                    

            }
        
            return render(request, 'medicines/view_medicine_details.html', context)
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
  

# --------------------------expire medicicne lisat ----------------------------------

def Expaire_medicine_list(request):
    try:
        if request.user.has_perm('Inventory.  view_medicine'):
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
                order =MedicineTransection.objects.filter(Expire_date__lte = today
                    # Q(Medicine_name__Medicine_name__icontains = SearchQuery)| 
                    # Q(Expire_date__icontains = SearchQuery) 
                    
                ).order_by('Expire_date') 
                order =MedicineTransection.objects.filter(
                 Q(MedId__Medicine_name__icontains = SearchQuery))
            else:
                order =MedicineTransection.objects.filter(Expire_date__lte = today)
                
            paginator = Paginator(order, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'order',
                'type' : type,
                'Status': Status,
                'expired':Expaire_medicine_list
            }
            return render(request, 'medicines/Expaire_medicine_list.html',context)  
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

#-----delete medicine -----------

def delete_medicine(request,Medicine_id):
    if request.user.has_perm('Inventory.view_medicine') or request.user.has_perm('Inventory.delete_medicine')  :

        medicine = Medicine.objects.get(pk=Medicine_id)
        medicine.delete()
        
        return redirect('medicines')
    else:
            return render(request, 'Hr/403.html')

#----------Lost and dameged -------------------------#
# def book_genre_count(request):
#     genres = Book.objects.values('genre').annotate(count=Count('id'))

#     return render(request, 'book_genre_count.html', {'genres': genres})


# def medicine_in(request):
#     # med_in = MedicineTransection.objects.values('purchase').annotate(count=Counter('id'))

#     med_in = Medicine.objects.filter(status__icontains='purchase')


#     return render(request,'medicine/med_in.html',{'med_in':med_in})


    
        
   