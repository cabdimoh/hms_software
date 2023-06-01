from django.db import models
from django.forms import CharField, MultiValueField, ValidationError
from django.urls import reverse
from django.db.models import Max
from django.core.validators import RegexValidator
from datetime import timedelta, datetime,date
import datetime
from Users import models as user_model
currentime = datetime.datetime.now()
from datetime import date
currentDate = date.today()
# Create your models here.


class Title(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=60,)
    father_name = models.CharField(max_length=60,)
    last_name = models.CharField(max_length=60,)
    mother_name = models.CharField(max_length=60,)
    gender = models.CharField(max_length=50,)
    marital = models.CharField(max_length=50,)
    emp_number = models.CharField(max_length=50,)
    Blood_Group = models.CharField(max_length=50, )
    dob = models.DateField()
    phone = models.CharField(max_length=1000)
    emergency_contect = models.BigIntegerField()
    email = models.EmailField()
    photo = models.ImageField(upload_to='images/profile')
    address = models.CharField(max_length=100)
    Employee_state = models.CharField(max_length=100, default='Pending')
    schedula = models.CharField(max_length=100, blank=True,null=True)    
    schedula_state = models.BooleanField(default=False ,blank=True,null=True)    
    is_terminated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)   
    
    appprovedwho = models.CharField(max_length=100, )
    job_type = models.ForeignKey('Title', on_delete=models.RESTRICT,)

    class Meta:
        permissions = [
            ("Approve_employee", "Can approve Employee"),
        ]

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('employee_details', args=[self.id])
    
    def get_absolute_url_print(self):
        return reverse('printemployee_data',args=[self.id])

    def get_full_name(self):
        return f"{self.first_name} {self.father_name} {self.last_name}"

    def add_space_to_phone_number(self):
        return self.phone[:2] + "-" + self.phone[2:]
    
    def checkpresent(self):
        checker = False
        today = date.today()
        day_name = today.strftime("%A")
        days = self.schedula.split(',')
        for d in days:
            if d == day_name:    
                checker = True  
                break
            else:
                checker = False
                   
        return checker
    
    def detect_attendance(self):
        result = 'not Attandance'
        get_attendance  =Attandence.objects.filter(employee=self.id , today_date = currentDate)
        if get_attendance.exists():
            result = ''      
            get_attendance = get_attendance[0]    
            result = 'Absent' if get_attendance.state == '0' else 'Present'      
        return result


class Banks(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class JobType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_appoitment_rel = models.CharField(max_length=100, )
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Salary(models.Model):
    name = models.CharField(max_length=300,)
    base_salary = models.FloatField()
    fixed_allow = models.FloatField(null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_type.name


class EmployeeBank(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    banks = models.ForeignKey(Banks, on_delete=models.RESTRICT)
    account_number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number

class   Directorate(models.Model):
    name = models.CharField(max_length=100, )
    Discriptions = models.CharField(max_length=400, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Secretary(models.Model):
    name = models.CharField(max_length=100, blank=True, )
    director = models.ForeignKey(Directorate, on_delete=models.RESTRICT, )
    Discriptions = models.CharField(max_length=400, )
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Qualification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    name = models.CharField(max_length=300, blank=True, null=True)
    Specialization = models.CharField(max_length=100, )
    Documents = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_document_detail(self):
        return get_image_description(self, self.Documents)

    def uploadedfile_url(self):
        if self.Documents and hasattr(self.Documents, 'url'):
            return self.Documents.url


class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    name = models.CharField(max_length=300, )
    place = models.CharField(max_length=100, )
    start = models.DateField()
    end = models.DateField()
    documents = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_document_detail(self):
        return get_image_description(self, self.documents)

    def uploadedfile_url(self):
        if self.documents and hasattr(self.documents, 'url'):
            return self.documents.url

    def __str__(self):
        return self.name


class Departments(models.Model):
    director = models.ForeignKey(Directorate, on_delete=models.RESTRICT, blank=True, null=True)
    department_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name


class Depart_Sections(models.Model):
    departments = models.ForeignKey(
        Departments, on_delete=models.RESTRICT, blank=True, null=True)
    department_sections = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_sections


class JobDetails(models.Model):
    job_type = models.ForeignKey(JobType, on_delete=models.RESTRICT)
    department_all = models.ForeignKey(
        Departments, on_delete=models.RESTRICT, blank=True, null=True)
    employee_type = models.CharField(max_length=200, blank=True, null=True)
    depar_section = models.ForeignKey(
        Depart_Sections, on_delete=models.RESTRICT, blank=True, null=True)
    director = models.ForeignKey(
        Directorate, on_delete=models.RESTRICT, blank=True, null=True)
    secretory = models.ForeignKey(
        Secretary, on_delete=models.RESTRICT,  blank=True, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, blank=True, null=True)
    salary = models.ForeignKey(Salary, on_delete=models.RESTRICT)
    base_pay = models.FloatField(default=0.0)
    appprovedwho = models.CharField(max_length=500, )
    TermsOfService = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    job_state = models.CharField(max_length=500, default="Pending")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.first_name


    def get_absolute_url(self):
        return reverse('printjobs', args=[self.id])


    def time_since_update(self):
        time_diff = self.update - self.created
        return time_diff.total_seconds()

    def getuserid(self):
        Result = False
        is_exist = user_model.Users.objects.filter(employee=self.employee)
        if is_exist.exists():
            Result = True

        return Result


class LeaveCatogory(models.Model): 
    name = models.CharField(max_length=100)
    n_days = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
        
    def get_modified_date(self):
        timedelta = getCurrentDate() - self.update
        seconds = timedelta.days * 24 * 3600 + timedelta.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"



class Employee_Leave(models.Model):  
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    leave_ct = models.ForeignKey(LeaveCatogory, on_delete=models.RESTRICT)
    startday = models.DateField()
    endtday = models.DateField()
    reason = models.TextField()
    State = models.CharField(default='Pending', max_length=100 , blank=True, null=True )
    document = models.FileField()
    leavesdays = models.CharField(max_length=100,blank=True, null=True)
    approvedBy = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.get_full_name()

    def get_modified_date(self):
        timedelta = getCurrentDate() - self.update
        seconds = timedelta.days * 24 * 3600 + timedelta.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"


    def start_format(self):
        return self.startday.strftime("%b %d, %Y ")
    def end_format(self):
        return self.endtday.strftime("%b %d, %Y ")
    
    def date_format(self):
        return self.created.strftime("%b %d, %Y %I:%M %p")



    def get_document_detail(self):
        return get_image_description(self, self.document)

    def uploadedfile_url(self):
        if self.document and hasattr(self.document, 'url'):
            return self.document.url

class Payroll(models.Model):
    JobDetails = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    EmployeeBank = models.ForeignKey(LeaveCatogory, on_delete=models.RESTRICT)  

class Work_shift(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.RESTRICT,)
    shift_name = models.CharField(max_length=100)
    shift_type = models.CharField(max_length=100,)
    shift_date = models.CharField(max_length=300,)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shift_name
    
    def get_absolute_url(self):
        return reverse('view_shifts', args=[self.id])


class Employee_exit_Category(models.Model):
    category_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    def time_since_update(self):
        time_diff = self.created - self.update
        seconds = time_diff.days * 24 * 3600 + time_diff.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"

        if hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

        if minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"


class exited_employee(models.Model):
    exit_emp = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    exit_emp_category = models.ForeignKey(
        Employee_exit_Category, on_delete=models.RESTRICT)
    reason = models.TextField()
    dayHappen = models.DateField(default='', blank=True, null=True)
    timeHappen = models.TimeField(default='', blank=True, null=True)
    document = models.FileField()
    exit_state = models.CharField(default='Pending', max_length=50)
    appprovedwho = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason

    def date_format(self):
        return self.created.strftime("%b %d, %Y %I:%M %p")
        # def formatted_created(self):
        # return self.created.strftime("%b %d, %Y %I:%M %p")

    def get_document_detail(self):
        return get_image_description(self, self.document)

    def uploadedfile_url(self):
        if self.document and hasattr(self.document, 'url'):
            return self.document.url






class Manage_shift(models.Model):
    shift = models.ForeignKey(Work_shift, on_delete=models.RESTRICT, )
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT, )   
    state = models.CharField(max_length=400, blank=True, null=True ,default='inactive')   
    existday = models.BooleanField(blank=True,null=True )
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.first_name
    
    def getAttendingOne(self):
        Result = False
       
        is_exist = Attandence.objects.filter(employee=self.employee)
        if is_exist.exists():
            Result = True
          
        return Result
    def get_attendance_date(self):
        Result = False
        
       
        is_attended_today = Attandence.objects.filter(employee=self.employee,today_date=currentDate)
        if is_attended_today.exists():
            get_info=is_attended_today[0]
            Result = True
            context={
            'attended' :Result,
            'id': get_info.id,
            'state':get_info.state
        }
        else:
             context={
            'attended' :Result
        }
          
        return context


class Attandence(models.Model):
    shift = models.ForeignKey(Work_shift, on_delete=models.RESTRICT, )
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT, )   
    state = models.CharField(max_length=100, )
    today_date = models.DateField()   
    reason = models.CharField(max_length=400, blank=True, null=True)   
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.get_full_name()
    
    def checkpresent(self):
        checker = ''
        today = date.today()
        day_name = today.strftime("%A")
        days = self.shift.shift.shift_date.split(',')
        for d in days:
            if d == day_name:    
                
                break
            else:
                checker = ''
                   
        return checker



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


def getCurrentDate():
    time = datetime.datetime.now(datetime.timezone.utc)
    return time

def get_modified_dates(timedelta): 
    seconds = timedelta.days * 24 * 3600 + timedelta.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if days > 0:
        return f"{days} {'day' if days == 1 else 'days'} ago"

    if hours > 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"

    if minutes > 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

    return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"
