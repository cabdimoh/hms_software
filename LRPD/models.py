
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse
# from APEN.models import Appointments
from Hr.models import Employee
from Users.models import Users
from datetime import datetime

# from Inventory.models import Medicine , Equipment 
# Create your models here.
#------------------Laboratory---------------------------

# class LabTestsCategory(models.Model):
#     CategoryName = models.CharField(max_length=100)
#     CategoryDescription = models.CharField(max_length=140)
#     created = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'LabTestsCategory'
        
#     def _str_(self):
#         return self.CategoryName
    
class LabTests(models.Model):
    TestName = models.CharField(max_length=100)
    TestDescription = models.CharField(max_length=140)
    SampleType = models.CharField(max_length=50)
    ShortName = models.CharField(max_length=100)
    TestNumber = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'LabTests'
        
    def _str_(self):
        return self.TestName
    def get_blood_properties(self):
        try:
            blood_properties = LabTest_Blood_Properties.objects.get(TestID=self)
            blood_properties_dict = model_to_dict(blood_properties)
        except LabTest_Blood_Properties.DoesNotExist:
            blood_properties_dict = None
        return blood_properties_dict
    def get_parameters_properties(self):
        try:
            parameters_properties = LabExaminationParameters.objects.get(TestID=self)
            parameters_properties_dict = model_to_dict(parameters_properties)
        except LabExaminationParameters.DoesNotExist:
            parameters_properties = None
        return parameters_properties_dict
        
    
class LabTestGroups(models.Model):
    GroupName = models.CharField(max_length=100)
    GroupDescription = models.CharField(max_length=140)
    sampleType = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'LabTestGroups'
        
    def _str_(self):
        return self.GroupName
    
class LabTestSubGroups(models.Model):
    SubGroupName = models.CharField(max_length=100)
    SubGroupDescription = models.CharField(max_length=140)
    Group = models.ForeignKey(LabTestGroups, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'LabTestSubGroups'
        
    def _str_(self):
        return self.SubGroupName


class LabTest_Blood_Properties(models.Model):
    TestID = models.ForeignKey(LabTests, on_delete=models.CASCADE)
    NormalRange = models.CharField(max_length=70)
    TestUnit = models.CharField(max_length=70)
    Group = models.ForeignKey(LabTestGroups, on_delete=models.CASCADE)
    SubGroup =  models.ForeignKey(LabTestSubGroups, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'LabTest_Blood_Properties'
        
    def _str_(self):
        return self.TestID.TestName
          
class LabTestOrders(models.Model):
    Admission = models.ForeignKey('APEN.Addmission', on_delete=models.SET_NULL, null=True)
    Appointment = models.ForeignKey('APEN.Appointments', on_delete=models.SET_NULL, null=True) 
    Visit = models.ForeignKey('APEN.EmergencyRoomVisit', on_delete=models.SET_NULL, null=True)
    Ordered_by = models.TextField()    
    Order_date = models.DateField(auto_now_add=True)
    Status = models.CharField(max_length=100)
    TestOrderNumber = models.CharField(max_length=100)
    class Meta:
        db_table = 'LabTestOrders'
        
    def _str_(self):
        return self.Test.TestName
    
    def get_absolute_url(self):
        return reverse('add-lab-result-form', args=[self.id])
    
    
class LabTestOrderDetails(models.Model):
    LabTestOrder = models.ForeignKey(LabTestOrders, on_delete=models.CASCADE)
    Test = models.ForeignKey(LabTests, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'LabTestOrderDetails'
        
    def _str_(self):
        return self.LabTestOrder

class LabEquipmentOrder(models.Model):
    Item = models.ForeignKey('Inventory.Equipment', on_delete=models.PROTECT)
    Quantity = models.IntegerField()
    Status = models.CharField(max_length=50)
    Ordered_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Order_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'LabEquipmentOrder'
        
    def _str_(self):
        return self.Item.item_name
    
class LabExaminationParameters(models.Model):
    Test = models.ForeignKey(LabTests, on_delete=models.PROTECT)
    Type = models.CharField(max_length=100)
    ParameterName = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'LabExaminationParameters'
        
    def _str_(self):
        return self.Test.TestName
    def id_increment(self):
        return reverse('add-lab-result-form', args=[self.id])
    
class LabTestResult(models.Model):
    LabTestOrder = models.ForeignKey(LabTestOrders, on_delete=models.CASCADE)
    Result_date = models.DateField(auto_now_add=True)
    CollectionDate = models.DateField()
    Collected_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="collected_by")
    Employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="employee")
    Comment = models.TextField()
    class Meta:
        db_table = 'LabTestResult'
        
    def _str_(self):
        return self.LabTestOrder

class Lab_Blood_Results(models.Model):
    labTest_result = models.ForeignKey(LabTestResult, on_delete=models.CASCADE)
    TestID = models.ForeignKey(LabTest_Blood_Properties, on_delete=models.CASCADE)
    ResultValue = models.CharField(max_length=200)
    flag = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = 'Lab_Blood_Results'
        
    def _str_(self):
        return self.labTest_result
            

class Lab_ExaminationParameters_Results(models.Model):
    labTest_result = models.ForeignKey(LabTestResult, on_delete=models.CASCADE)
    TestID = models.ForeignKey(LabTests, on_delete=models.CASCADE)
    ResultValue = models.CharField(max_length=200)
    Parameter = models.ForeignKey(LabExaminationParameters, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'Lab_ExaminationParameters_Results'
        
    def _str_(self):
        return self.labTest_result
            
#------------------Radiology---------------------------
class ExamCategory(models.Model):
    CategoryName = models.CharField(max_length=150)
    Description = models.TextField()
    class Meta:
        db_table = 'ExamCategory'
        
    def _str_(self):
        return self.CategoryName
class RadiologyExam(models.Model):
    Category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE)
    ExamName = models.CharField(max_length=100)
    ExamDescription = models.CharField(max_length=140) 
    ExamNumber = models.CharField(max_length=100)
    Created = models.DateTimeField(auto_now_add=True)
    Update = models.DateTimeField(auto_now=True)   
    class Meta:
        db_table = 'RadiologyExam'
        
    def _str_(self):
        return self.ExamName


class RadiologyOrders(models.Model):
    Admission = models.ForeignKey('APEN.Addmission', on_delete=models.SET_NULL, null=True)
    Appointment = models.ForeignKey('APEN.Appointments', on_delete=models.SET_NULL, null=True) 
    Visit = models.ForeignKey('APEN.EmergencyRoomVisit', on_delete=models.SET_NULL, null=True)
    Ordered_by = models.TextField()
    Order_date = models.DateField(auto_now_add=True)
    Status = models.CharField(max_length=100)
    RadiologyOrderNumber = models.CharField(max_length=100)
    class Meta:
        db_table = 'RadiologyOrder'
        
    def _str_(self):
        return self.RadiologyExam.ExamName
    def get_absolute_url(self):
        return reverse('add-radio-result-form', args=[self.id])
    
    
class RadiologyOrderDetails(models.Model):
    RadiologyOrder = models.ForeignKey(RadiologyOrders, on_delete=models.CASCADE)
    RadiologyExam = models.ForeignKey(RadiologyExam, on_delete=models.SET_NULL, null=True)    
    class Meta:
        db_table = 'RadiologyOrderDetails'
        
    def _str_(self):
        return self.RadiologyOrder
    
    
class RadiologyResult(models.Model):
    RadiologyOrder = models.ForeignKey(RadiologyOrders, on_delete=models.CASCADE)
    Result_date = models.DateField(auto_now_add=True)
    CollectionDate = models.DateField()
    Collected_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="collected_by_radio")
    Employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="employee_radio")
    class Meta:
        db_table = 'RadiologyResult'
        
    def _str_(self):
        return self.RadiologyOrder

class RadiologyResultDetails(models.Model):
    Radiology_Result = models.ForeignKey(RadiologyResult, on_delete=models.CASCADE)
    RadiologyExam = models.ForeignKey(RadiologyExam, on_delete=models.CASCADE)
    Findings = models.TextField()
    Impressions = models.TextField()
    Recommendations = models.TextField()
    Comments = models.TextField()
    Result_Files = models.FileField(null=True)
    class Meta:
        db_table = 'RadiologyResultDetails'
        
    def _str_(self):
        return self.RadiologyResult
    def get_document_detail(self):
        return get_image_description(self, self.Result_Files)

    def uploadedfile_url(self):
        if self.Result_Files and hasattr(self.Result_Files, 'url'):
            return self.Result_Files.url
class RadiologyEquipmentOrder(models.Model):
    Item = models.ForeignKey('Inventory.Equipment', on_delete=models.PROTECT)
    Quantity = models.IntegerField()
    Status = models.CharField(max_length=50)
    Ordered_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Order_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'RadiologyEquipmentOrder'
        
    def _str_(self):
        return self.Item.item_name


#------------------Pharmacy--------------------------

class MedicineOrder(models.Model):
    
    Order_Date = models.DateField(auto_now_add=True)
    Ordered_BY =  models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Status = models.CharField(max_length=100)
    

    class Meta:
        db_table = 'MedicineOrder'
        
    def _str_(self):
        return self.MedicineOrder
    

class MedicineOrderDetails (models.Model):
    medicineOrderid = models.ForeignKey(MedicineOrder, on_delete=models.CASCADE)
    Medicine_name = models.ForeignKey('Inventory.Medicine', on_delete=models.SET_NULL, null=True) 
    box = models.PositiveIntegerField()
    

    class Meta:
        db_table = 'MedicineOrderDetails'
        
    def _str_(self):
        return self.MedicineOrderDetails.Medicine_name
     
class pharmacy_medicine (models.Model):
    Medicine_name = models.ForeignKey('Inventory.Medicine', on_delete=models.SET_NULL, null=True) 
    Medicine_categories =   models.ForeignKey('Inventory.Medicine_categories',on_delete=models.SET_NULL, null=True)  
    box =  models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    Expire_date = models.DateField()
    Total_quantity = models.PositiveIntegerField()  
    status = models.CharField(max_length=100)  

    def is_expired1(self):
        return self.Expire_date < datetime.now().date()

    class Meta:
        db_table = 'pharmacy_medicine'
    def get_pharmacy_medicine_details_url(self):
        return reverse('view-medicine', args=[self.id])
        
    def _str_(self):
        return self.MedicineOrderDetails.Medicine_nam

class PharmacyTransection(models.Model):
    PhMedId = models.ForeignKey(pharmacy_medicine,on_delete=models.SET_NULL, null=True)
    Type = models.CharField(max_length=100)
    box = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    Total_quantity = models.PositiveIntegerField()
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
        db_table = 'PharmacyTransection'
    
    
    def __str__(self):
        return self.Type
    
    
    
def get_image_description(image_self, image_url):
    try:

        if image_url is not None or image_url != '' or image_url != "null":
            file = image_url
            split_file = file.name.split('/')[-1].split('.')

            icon = 'bx bx-trash'
            color = 'primary'

            if split_file[1].lower() == 'pdf':
                icon = 'bx bxs-file-pdf'
                color = 'danger'

            if split_file[1].lower() == 'ppt' or split_file[1].lower() == 'pptx':
                icon = ' las la-file-alt'
                color = 'danger'

            if split_file[1].lower() == 'doc' or split_file[1].lower() == 'docx':
                icon = ' las la-file-alt'
                color = 'secondary'

            if split_file[1].lower() == 'png' or split_file[1].lower() == 'jpg' or split_file[1].lower() == 'jpeg':
                icon = 'las la-image'
                color = 'success'

            if split_file[1].lower() == 'txt':
                icon = ' las la-file-alt'
                color = 'dark'

            if split_file[1].lower() == 'xlsx':
                icon = 'las la-file-alt'
                color = 'success'

            return {
                'size': pretty_size(file.size),
                'extension': split_file[1].upper(),
                'name': split_file[0],
                'icon': icon,
                'color': color,
                'url': image_self.uploadedfile_url()
            }
    except (FileNotFoundError, IndexError, AttributeError):
        return {
            'size': "",
            'extension': "",
            'name': "",
            'icon': "",
            'color': "",
            'url': ""
        }


    # bytes pretty-printing
UNITS_MAPPING = [
    (1 << 50, ' PB'),
    (1 << 40, ' TB'),
    (1 << 30, ' GB'),
    (1 << 20, ' MB'),
    (1 << 10, ' KB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix