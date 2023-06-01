from datetime import timezone
import datetime
from django.urls import reverse
from django.db import models
from Hr.models import Employee
from LRPD import models as model_inventory
from django.db.models import Sum
from datetime import datetime
# Create your models here.

class Equipment_categories(models.Model):
    category_name = models.CharField(max_length=40)
    discription = models.CharField(max_length=100)

    class Meta:
        db_table = 'Equipment_categories'
        
    def __str__(self):
        return self.category_name

class Equipment(models.Model):
    item_name = models.CharField(max_length=40)
    category = models.ForeignKey(Equipment_categories,on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    lost_and_damaged = models.IntegerField()
    manufacturing = models.CharField(max_length=100)
    supplier_price = models.FloatField()
    
    employe = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    def get_equipment_details_url(self):
        return reverse('equipment-View', args=[self.id])
    
    class Meta:
        db_table = 'Equipment'
    def __str__(self):
        return self.item_name
    
    
    
    

class EquipmentTransection(models.Model):
    EqId  = models.ForeignKey(Equipment,on_delete=models.SET_NULL, null=True)
    Type = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    lost_and_damaged= models.IntegerField()
    manufacturing = models.CharField(max_length=100)
    supplier_price = models.FloatField()
    Transectno = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    

    class Meta:
        db_table = 'EquipmentTransection'
    def __str__(self):
        return self.Type


class Medicine_categories(models.Model):
    medicine_cat_name = models.CharField(max_length=40)
    discription = models.CharField(max_length=100)

    class Meta:
        db_table = 'medicine_categories'
        
    def __str__(self):
        return self.medicine_cat_name

class Medicine(models.Model):
    Medicine_name = models.CharField(max_length=100)
    
    Medicine_categories = models.ForeignKey(Medicine_categories,on_delete=models.SET_NULL, null=True)
    box = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    dosage = models.CharField(max_length=100)
    manufacturing = models.CharField(max_length=100)
    
    supplier_price = models.FloatField()
    status = models.CharField(max_length=100)

    def get_medicine_details_url(self):
        return reverse('medicine-View1', args=[self.id])
    
    def save(self, *args, **kwargs):
        if self.box == 0:
            self.status = 'not available'
        else:
            self.status = 'Available'
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'Medicine'
    def __str__(self):
        return self.Medicine_name
    


    # def get_purchase_stock(self):
    #     transactions = MedicineTransection.objects.filter(MedId=self)
    #     purchase_stock = 0
    #     for transaction in transactions:
    #         if transaction.Type == 'purchase':
    #             purchase_stock += transaction.box
    #         elif transaction.Type == 'paid':
    #             purchase_stock -= transaction.box
        
    #     return purchase_stock
    # def get_refill_stock(self):
    #     transactions = MedicineTransection.objects.filter(MedId=self)
    #     refill_stock = 0
    #     for transaction in transactions:
         
    #         if transaction.Type == 'Refill':
    #             refill_stock += transaction.box
    #         elif transaction.Type == 'paid':
    #             refill_stock -= transaction.box
    #     return refill_stock
    
    # def get_latest_batch_number(self):
    #     latest_transaction = MedicineTransection.objects.filter(MedId=self).order_by('-date', '-BatchNO').first()
    #     return latest_transaction.BatchNO if latest_transaction else None
    # def get_available_batch_number(self):
    #     transactions = MedicineTransection.objects.filter(MedId=self).order_by('date', 'BatchNO')
    #     latest_batch_number = self.get_latest_batch_number()
        
    #     last_num = int(latest_batch_number[1:])
    #     next_num = str(last_num + 1).zfill(3)
    #     available_batch = None
    #     for transaction in transactions:
    #         if transaction.Type == 'purchase' and transaction.box > 0 and transaction.status=="open":
    #             available_batch = transaction.BatchNO
    #             break
    #         elif transaction.Type == 'Refill' and transaction.box > 0  and transaction.status=="open":
    #             available_batch = transaction.BatchNO
    #             break   # Stop searching after the first available refill transaction is found
    #     if available_batch:
    #         return available_batch
    #     else:
    #         # If no available refill transactions are found, use the next batch number
    #         return '0' + next_num
class MedicineTransection(models.Model):
    MedId = models.ForeignKey(Medicine,on_delete=models.SET_NULL, null=True)
    Type = models.CharField(max_length=100)
    box = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    manufacturing_date = models.DateField()
    BatchNO = models.CharField(max_length=100)
    supplier_price = models.CharField(max_length=100)
    Expire_date = models.DateField()
    
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    
    
    employe = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    def is_expired(self):
        return self.Expire_date < datetime.now().date()

    def days_until_expiry(self):
        expiry_delta = self.Expire_date - datetime.now().date()
        return expiry_delta.days

    class Meta:
        db_table = 'MedicineTransection'
    def __str__(self):
        return self.Type




class lost_and_dameged_equipment(models.Model):
    Equipment_name = models.ForeignKey(Equipment,on_delete=models.SET_NULL, null=True)
    lost_and_damaged = models.PositiveIntegerField()
    reason= models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'lost_and_dameged_equipment'
    def __str__(self):
        return self.Equipment_name





#
   

    




        






    





 #def get_balance(self):
    #     get_orders=model_inventory.MedicineOrderDetails.objects.filter(medicineOrderid__Status="Approved",Medicine_name=self.id).aggregate(Sum('box'))['box__sum']
       
        
    #     if get_orders is None:
    #         get_orders=0 
    #     else:
    #         get_orders=get_orders
    #     total=self.box+get_orders
    #     cont={
    #         'balance':get_orders,
    #         'total':total
    #     }
    #     return cont