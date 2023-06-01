import re
from django.shortcuts import render , redirect

from APEN import models
from .models import EquipmentTransection, Medicine ,Medicine_categories , Equipment_categories , Equipment , MedicineTransection
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from LRPD.models import MedicineOrder , MedicineOrderDetails ,LabEquipmentOrder, pharmacy_medicine ,PharmacyTransection
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Case, When
from django.db import models





#----------generated numbers------equipment

def GenerateSerialNumber():
    last_id = EquipmentTransection.objects.filter(~Q(Transectno=None)).last()
    serial = 0
    if last_id is not None and last_id.Transectno.startswith('TRS'):
        serial = int(last_id.Transectno[4:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"TRS{serial}"


# #------------MEDICINE ORDER--------
@login_required(login_url='Login')
def medicine_order(request):
    if request.user.has_perm('Inventory.view_medicine'):
    
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
                Q(Order_Date__icontains = SearchQuery) |
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
        return render (request, 'medicines/GetMedicineOder.html',context)
    else:
            return render(request, 'Hr/403.html')
#---------------medicine order accepeted------------------------------------------------------
@login_required(login_url='Login')
def manage_order_medicine(request,action):
    if request.user.has_perm('Inventory.view_medicine'):

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
                    'Status':new_medicine_order.Status

                }
            return JsonResponse({'isError': False, 'Message': message}, status=200)
        

        if action == "get_approvers":
            if request.method == 'POST':
                id = request.POST.get('OrderId')
                
                Status = "Approved" 
                medid= MedicineOrder.objects.get(id=id)
                medid.Status = Status
                medid.save()
                # print(medid.id)
                all_baches=[]
                all_boxes=[]
                total_paid_boxes=[]
                paid_boxes=[]
                total = 0 
                main_medidne_details= MedicineOrderDetails.objects.filter(medicineOrderid=medid.id)
                for med1 in main_medidne_details:
                    
                    old_med_box1= med1.Medicine_name.box
                    new_med_box1 = med1.box
                    total1 = old_med_box1 - new_med_box1
                    item = Medicine.objects.get(id= med1.Medicine_name.id)
                    item.box = total1
                    item.save()
            
                med_details= MedicineOrderDetails.objects.filter(medicineOrderid=medid.id)
                all_batchs = []
                paid_box_sum = 0
                in_box_sum = 0
                remaining_box = 0
                new_transection={}

                process_second_set = False
                for med in med_details:
                    ordered_box = med.box
                    medicine = Medicine.objects.get(id=med.Medicine_name.id)
                    med_trans = MedicineTransection.objects.filter(
                        MedId=medicine.id,
                        Type__in=['purchase', 'Refill'],
                    )

                    # Extract BatchNO from the MedicineTransections
                    batch_nos = med_trans.values_list('BatchNO', flat=True)

                    # Print the BatchNOs
                    available_box = 0
                    for batch_no in batch_nos:
                        paid_trans = MedicineTransection.objects.filter(Type="paid", BatchNO=batch_no)
                        in_trans = MedicineTransection.objects.exclude(Type="paid").get(BatchNO=batch_no)  

                        paid_box_sum = paid_trans.aggregate(box_sum=models.Sum('box'))['box_sum']
                        in_box_sum = in_trans.box

                        if paid_box_sum:
                            available_box = in_box_sum - paid_box_sum
                        else:
                            available_box = in_box_sum
                        if available_box >= ordered_box:
                            
                            paid = MedicineTransection(
                                MedId_id=medicine.id,
                                Type='paid',
                                box=ordered_box,
                                qty=in_trans.qty,
                                manufacturing_date=in_trans.manufacturing_date,
                                BatchNO=in_trans.BatchNO,
                                supplier_price=in_trans.supplier_price,
                                Expire_date=in_trans.Expire_date,
                                status="open"
                            )
                            paid.save()
                            new_transection.update({
                                'manufacting_date':in_trans.manufacturing_date,
                                'expire_date':in_trans.Expire_date,
                                'batch_no':in_trans.BatchNO,
                                'supplier_price':in_trans.supplier_price,
                                'qty':in_trans.qty
                                


                            })
                            # Add your logic here

                            break  # Exit the loop as soon as available_box is greater than 0
                        elif available_box < ordered_box and available_box != 0:
                            remaining_box = ordered_box - available_box
                            paid = MedicineTransection(
                                MedId_id=medicine.id,
                                Type='paid',
                                box=ordered_box - remaining_box,
                                qty=in_trans.qty,
                                manufacturing_date=in_trans.manufacturing_date,
                                BatchNO=in_trans.BatchNO,
                                supplier_price=in_trans.supplier_price,
                                Expire_date=in_trans.Expire_date,
                                status="open"
                            )
                            paid.save()
                            new_transection.update({
                                'manufacting_date':in_trans.manufacturing_date,
                                'expire_date':in_trans.Expire_date,
                                'batch_no':in_trans.BatchNO,
                                'supplier_price':in_trans.supplier_price,
                                'qty':in_trans.qty


                            })

                            # update row to empty
                            in_trans.status = "empty"
                            in_trans.save()

                            process_second_set = True
                            break
                    if process_second_set:
                        available_box = 0 
                        process_second_set = False
                        for batch_no in batch_nos:
                            paid_trans = MedicineTransection.objects.filter(Type="paid", BatchNO=batch_no)
                            in_trans = MedicineTransection.objects.exclude(Type="paid").get(BatchNO=batch_no)

                            paid_box_sum = paid_trans.aggregate(box_sum=models.Sum('box'))['box_sum']
                            in_box_sum = in_trans.box
                            if paid_box_sum:
                                available_box = in_box_sum - paid_box_sum
                            else:
                                available_box = in_box_sum
                            if remaining_box > 0:
                                if available_box >= remaining_box:
                                    paid = MedicineTransection(
                                        MedId_id=medicine.id,
                                        Type='paid',
                                        box=remaining_box,
                                        qty=in_trans.qty,
                                        manufacturing_date=in_trans.manufacturing_date,
                                        BatchNO=in_trans.BatchNO,
                                        supplier_price=in_trans.supplier_price,
                                        Expire_date=in_trans.Expire_date,
                                        status="open"
                                    )
                                    paid.save()
                                    new_transection.update({
                                    'manufacting_date':in_trans.manufacturing_date,
                                    'expire_date':in_trans.Expire_date,
                                    'batch_no':in_trans.BatchNO,
                                    'supplier_price':in_trans.supplier_price,
                                    'qty':in_trans.qty


                                    })
                                    break
                              
                                elif available_box < remaining_box and available_box != 0:
                                    remaining_box = remaining_box - available_box
                                    paid = MedicineTransection(
                                        MedId_id=medicine.id,
                                        Type='paid',
                                        box=ordered_box - remaining_box,
                                        qty=in_trans.qty,
                                        manufacturing_date=in_trans.manufacturing_date,
                                        BatchNO=in_trans.BatchNO,
                                        supplier_price=in_trans.supplier_price,
                                        Expire_date=in_trans.Expire_date,
                                        status="open"
                                    )
                                    paid.save()
                                    new_transection.update({
                                    'manufacting_date':in_trans.manufacturing_date,
                                    'expire_date':in_trans.Expire_date,
                                    'batch_no':in_trans.BatchNO,
                                    'supplier_price':in_trans.supplier_price,
                                    'qty':in_trans.qty


                                    })

                                    # update row to empty
                                    in_trans.status = "empty"
                                    in_trans.save()

                                    process_second_set = True
                            
                                    

                                # Add your logic here
                    print(new_transection)
                    type = "our_order"
                    # PhaT = PharmacyTransection.objects.filter(PhMedId=med.Medicine_name.MedId.id) .first()
                    # expire_date = PharmacyTransection.PhMedId.medicine_transactions.first().Expire_date
                    total_quantity = med.box * int(new_transection['qty'])
            
                    if medid.Status == "Approved":
                        old_med = pharmacy_medicine.objects.filter(Medicine_name_id=med.Medicine_name.id)
                        
                        if old_med:
                            for o_med in old_med:
                                old_total_qty =o_med.Total_quantity
                                qty = new_transection['qty']
                                ordered_new_box = med.box
                                new_total_qty = ordered_new_box * qty
                                print(old_total_qty)
                                print(new_total_qty)
                                print(new_transection['qty'])
                                
                                update_pharmacy_medicine = pharmacy_medicine.objects.get(id=o_med.id)
                                update_pharmacy_medicine.box = o_med.box + med.box
                                update_pharmacy_medicine.Expire_date = new_transection['expire_date']
                                update_pharmacy_medicine.Total_quantity = int(new_total_qty) + int(old_total_qty)
                                update_pharmacy_medicine.save()

                            
                                pharmacy_tarnsaction = PharmacyTransection(
                                    PhMedId_id=o_med.id,
                                    Type=type,box=med.box,
                                    quantity= new_transection['qty'],
                                    Total_quantity=total_quantity,
                                    manufacturing_date=new_transection['manufacting_date'],
                
                                    BatchNO=new_transection['batch_no'],
                                    supplier_price=new_transection['supplier_price'],
                                    Expire_date=new_transection['expire_date'],
                                    status=item.status)
                                pharmacy_tarnsaction.save()
                               
                              
                        else:
                            new_pharmacy_medicine = pharmacy_medicine(Medicine_name_id = med.Medicine_name.id ,Medicine_categories_id=med.Medicine_name.Medicine_categories.id,
                            box= med.box, quantity = new_transection['qty'],Expire_date=new_transection['expire_date'], Total_quantity =total_quantity, status = "Available"  )
                            new_pharmacy_medicine.save()
                            
                            curent_pharmcy = pharmacy_medicine.objects.get(id=new_pharmacy_medicine.id)
                            pharmacy_tarnsaction = PharmacyTransection(
                                    PhMedId_id=curent_pharmcy.id,
                                    Type=type,box=med.box,
                                    quantity= new_transection['qty'],
                                    Total_quantity=total_quantity,
                                    manufacturing_date=new_transection['manufacting_date'],
                
                                    BatchNO=new_transection['batch_no'],
                                    supplier_price=new_transection['supplier_price'],
                                    Expire_date=new_transection['expire_date'],
                                    status=item.status)
                            pharmacy_tarnsaction.save()

            else:
                return render(request, 'Hr/403.html')  
            return JsonResponse(
                {
                        'isError': False,
                        'Message': 'Your request approved',
                        'title': "masha allah ! been updated",
                        'type': 'success',
                    }
                )  



        if request.method == 'POST':
            id = request.POST.get('OrderId')
            
            Status = "Approved" 
            medid= MedicineOrder.objects.get(id=id)
            medid.Status = Status
            medid.save()
            # print(medid.id)
            all_baches=[]
            all_boxes=[]
            total_paid_boxes=[]
            paid_boxes=[]
            total = 0 
            main_medidne_details= MedicineOrderDetails.objects.filter(medicineOrderid=medid.id)
            for med1 in main_medidne_details:
                
                old_med_box1= med1.Medicine_name.box
                new_med_box1 = med1.box
                total1 = old_med_box1 - new_med_box1
              
            
                
                
               
                item = Medicine.objects.filter(id= med1.Medicine_name.id).first()
                item.box = total1
                item.save()
           
            med_details= MedicineOrderDetails.objects.filter(medicineOrderid=medid.id)
            for med in med_details:
                item = MedicineTransection.objects.filter(MedId= med.Medicine_name.MedId.id).first()
                ordered_box = med.box
                bachs = MedicineTransection.objects.filter(
                 (Q(Type__icontains = "refill") |  Q(Type__icontains = "purchase"))   & Q(MedId= med.Medicine_name.MedId.id)  )
                paid_batches = MedicineTransection.objects.filter(
                 Q(Type__icontains = "paid")   & Q(MedId= med.Medicine_name.MedId.id)  )
                for paid_p in paid_batches:
                    paid_boxes.append(paid_p.box)

                for j in range(0, len(paid_boxes)):
                    total +=paid_boxes[j]
                    j+=1
                    
                    


                
                for b in bachs:
                    all_baches.append(b.BatchNO)
                    all_boxes.append(b.box)
                for i in range(0, len(all_baches)):
                   
                    if ordered_box > total:
                        remaining_box = ordered_box - (total)
                        type = "Stock Out"
                        paid = MedicineTransection(MedId_id=med.Medicine_name.MedId.id,Type=type,box=remaining_box,qty=item.qty,manufacturing_date=item.manufacturing_date,BatchNO=item.BatchNO,supplier_price=item.supplier_price,Expire_date=item.Expire_date,status=item.status)
                        paid.save() 
                        i+=1
                        


                    else:
                        type = "Stock Out"
                        paid = MedicineTransection(MedId_id=med.Medicine_name.MedId.id,Type=type,box=med.box,qty=item.qty,manufacturing_date=item.manufacturing_date,BatchNO=item.BatchNO,supplier_price=item.supplier_price,Expire_date=item.Expire_date,status=item.status)
                        paid.save() 
                 
                 
                # type = "our_order"
                type = "our_order"
            
                PhaT = PharmacyTransection.objects.filter(PhMedId=med.Medicine_name.MedId.id) .first()
                total_quantity = med.box * med.Medicine_name.MedId.quantity 
           
                if medid.Status == "Approved":
                    
                    old_med = pharmacy_medicine.objects.filter(Medicine_name_id=med.Medicine_name.MedId.id)
                    if old_med:
                        if old_med.Medicine_name.MedId.Medicine_name ==med.Medicine_name:
                            for o_med in old_med:
                                add_qty =o_med.box + med.box 
                                new_total_qty = add_qty * med.Medicine_name.MedId.quantity
                                update_pharmacy_medicine = pharmacy_medicine.objects.get(Medicine_name_id=med.Medicine_name.MedId.id)
                                update_pharmacy_medicine.box = add_qty
                                update_pharmacy_medicine.Expire_date = med.Medicine_name.Expire_date
                                update_pharmacy_medicine.Total_quantity = new_total_qty
                                update_pharmacy_medicine.save()
                            
                                pharmacy_tarnsaction = PharmacyTransection(PhMedId_id=med.Medicine_name.MedId.id,Type=type,box=med.box,quantity= med.Medicine_name.MedId.quantity,Total_quantity=total_quantity,manufacturing_date=item.manufacturing_date
                                ,BatchNO=item.BatchNO,supplier_price=item.supplier_price,
                                Expire_date=item.Expire_date,status=item.status)
                                pharmacy_tarnsaction.save()

                    else:
                        new_pharmacy_medicine = pharmacy_medicine(Medicine_name_id = med.Medicine_name.id ,Medicine_categories_id=med.Medicine_name.MedId.Medicine_categories.id,
                        box= med.box, quantity = med.Medicine_name.MedId.quantity,Expire_date=med.Medicine_name.Expire_date, Total_quantity =total_quantity, status = "Available"  )
                        new_pharmacy_medicine.save()
                        
                        curent_pharmcy = pharmacy_medicine.objects.get(id=new_pharmacy_medicine.id)
                        pharmacy_tarnsaction = PharmacyTransection(PhMedId_id=curent_pharmcy.id,Type=type,box=med.box,quantity= med.Medicine_name.MedId.quantity,Total_quantity=total_quantity,manufacturing_date=item.manufacturing_date
                        ,BatchNO=item.BatchNO,supplier_price=item.supplier_price,
                        Expire_date=item.Expire_date,status='avalibale')
                        pharmacy_tarnsaction.save()

            print(all_baches)
            print(paid_boxes)
            print(total_paid_boxes)
            print(total)
            return JsonResponse(
                {
                        'isError': False,
                        'Message': 'Your request approved',
                        'title': "masha allah ! been updated",
                        'type': 'success',
                    }
                )  
    
 









#-------------------------------dashbord------------------------



























