from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from .views import *
from .models import *
# from APEN.models import Specialities
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re
from datetime import date

# Get today's date

@login_required(login_url='Login')
def employees(request):
    try:
        if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Checkdepartment = 'depName' in request.GET
            Jobtitle = 'All'
            depName = 'All'
            DataNumber = 30
            SearchQuery = ''
            EmployeeList = []

            if Checkjobtitle:
                Jobtitle = request.GET['Jobtitle']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['job_type_id'] = Jobtitle

            if Checkdepartment:
                depName = request.GET['depName']

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            dataFilterings = {}
            if depName != 'All':
                dataFilterings['department_all_id'] = depName
            

            getdetpartment = JobDetails.objects.filter(**dataFilterings, is_active = True, job_state = "Approved").values('employee').distinct()

            print(getdetpartment)
            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee.objects.filter(
                    Q(id__in = getdetpartment),
                    Q(emp_number__icontains=SearchQuery) |
                    Q(job_type__name__icontains=SearchQuery) |
                    Q(first_name__icontains=SearchQuery) |
                    Q(father_name__icontains=SearchQuery) |
                    Q(last_name__icontains=SearchQuery) |
                    Q(emp_number__icontains=SearchQuery) |
                    Q(gender__icontains=SearchQuery),
                    **dataFiltering,
                    Employee_state="Approved",
                    is_terminated=False,
                    



                )
            else:
                EmployeeList = Employee.objects.filter(
                  Q(id__in = getdetpartment), **dataFiltering,     Employee_state="Approved", is_terminated=False)

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            emplNumber = Employee.objects.filter(
                Employee_state="Approved", is_terminated=False)

            emplmu = len(emplNumber)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,
                'pageTitle': 'Employee List',
                'job_types': Title.objects.all(),
                'alldep': Departments.objects.all(),
                'depName':depName,

                'employeeNumber': emplmu



            }
            return render(request, 'Hr/Employee.html', context)

        else:
            return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)

@login_required(login_url='Login')
def employeGalery(request):
    try:
        if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Jobtitle = 'All'
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if Checkjobtitle:
                Jobtitle = request.GET['Jobtitle']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['job_type_id'] = Jobtitle

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee.objects.filter(
                    Q(emp_number__icontains=SearchQuery) |
                    Q(job_type__name__icontains=SearchQuery) |
                    Q(first_name__icontains=SearchQuery) |
                    Q(father_name__icontains=SearchQuery) |
                    Q(last_name__icontains=SearchQuery) |                   
                    Q(gender__icontains=SearchQuery),
                    **dataFiltering,
                    Employee_state="Approved",
                    is_terminated=False



                )
            else:
                EmployeeList = Employee.objects.filter(
                    **dataFiltering,     Employee_state="Approved", is_terminated=False)

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            emplNumber = Employee.objects.filter(
                Employee_state="Approved", is_terminated=False)

            emplmu = len(emplNumber)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,
                'pageTitle': 'Employee List',
                'job_types': Title.objects.all(),

                'employeeNumber': emplmu



            }
            return render(request, 'Hr/empGalery.html', context)

        else:
            return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)


@login_required(login_url='Login')
def Pending_employees(request):
    try:
        if request.user.has_perm('Hr.Approve_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Jobtitle = 'All'
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if Checkjobtitle:
                Jobtitle = request.GET['Jobtitle']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['Employee_state'] = Jobtitle

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee.objects.filter(
                    Q(job_type__name__icontains=SearchQuery) |
                    Q(first_name__icontains=SearchQuery) |
                    Q(id__icontains=SearchQuery) |
                    Q(gender__icontains=SearchQuery),
                    ~Q(Employee_state="Approved"),
                    **dataFiltering,
                    is_terminated=False




                )
            else:
                EmployeeList = Employee.objects.filter(~Q(Employee_state="Approved"),
                                                       **dataFiltering,  is_terminated=False)

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            emplNumber = Employee.objects.all()
            emplmu = len(emplNumber)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,
                'pageTitle': 'Employee List',
                'job_types': JobType.objects.all(),
                'employeeNumber': emplmu



            }
            return render(request, 'Hr/Pending_Employee.html', context)
        else:
            return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)

@login_required(login_url='Login')
def view_Employee(request, pk):
    try:
        if request.user.has_perm('Hr.view_employee'):
            is_employee = Employee.objects.filter(id=pk).exists()
            if is_employee:
                single_employee = Employee.objects.get(id=pk)
                rate = 20
                qualification = Qualification.objects.filter(employee=pk)
                countQualif = len(qualification)
                if countQualif > 0:
                    rate += (countQualif * 0 + 20)
             
                job = JobDetails.objects.filter(employee=pk, is_active =True)
                countJob = len(job)              
                if countJob > 0:
                    rate += (countJob * 0 + 20)
             
                experiences = Experience.objects.filter(employee=pk)
                countExper = len(experiences)
                if countExper > 0:
                    rate += (countExper * 0 + 20)
             

                employee_Banks = EmployeeBank.objects.filter(employee=pk)
                countAccount = len(employee_Banks)
                if countAccount > 0:
                    rate += (countAccount * 0 + 20)
             
                today = date.today()

                # Get the day name
                day_name = today.strftime("%A")

               
                                
                context = {'single_employee': single_employee,
                        'id': pk,
                        'qualifications': qualification,
                        'experiences': experiences,
                        'employeeBanks': employee_Banks,
                        'job_types': Title.objects.all(),
                        'job_type_all': JobType.objects.all(),
                        'job_Details': JobDetails.objects.filter(employee=pk, is_active=True),
                        'job_Details_inactive': JobDetails.objects.filter(employee=pk, is_active=False, job_state='inactive'),
                        'salaries': Salary.objects.all(),
                        'all_banks': Banks.objects.filter(),
                        'salaries': Salary.objects.all(),
                        'all_department': Departments.objects.all(),
                        'all_Section': Depart_Sections.objects.all(),
                        'diractrates': Directorate.objects.all(),
                        'secretory': Secretary.objects.all(),
                        'attandence_all': Attandence.objects.filter(employee_id = pk),
                        'isError': False,
                        'True': True,
                        'countJob':countJob,
                        'countQualif':countQualif,
                        'countExper':countExper,
                        'countAccount':countAccount,
                        'rate':rate,
                        'day_name': day_name

                        }
                return render(request, 'Hr/employee_profile.html', context)
            else:
                return render(request, 'Hr/404.html')
        else:
            return render(request, 'Hr/400.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)

@login_required(login_url='Login')
def manage_employee(request, action):
    try:
        if request.method == 'POST':
            # This action will create a new account
            if action == 'new_employee':
                if request.user.has_perm('Hr.add_employee'):
                    # Get all data from the request
                    first_name = request.POST.get('first_name')
                    father_name = request.POST.get('father_name')
                    last_name = request.POST.get('last_name')
                    mother_name = request.POST.get('mother_name')
                    gender = request.POST.get('gender')
                    marital = request.POST.get('marital')
                    Dob = request.POST.get('Dob')
                    phone = request.POST.get('phone')
                    email = request.POST.get('email')
                    address = request.POST.get('address')
                    emergency_contect = request.POST.get('emergency_contect')
                    speciality = request.POST.get('speciality')

                    Blood_Group = request.POST.get('Blood_Group')
                    try:
                        file = request.FILES['photo']
                    except KeyError:
                        file = None
                    if file is None or file == '':
                        message = {
                            'isError': True,
                            'title': "Validation Error",
                            'type': "warning",
                            'Message': 'Please upload photo.'
                        }
                        return JsonResponse(message, status=200)

                    extention = file.name.split(".")[-1]
                    extention = extention.lower()
                    extension_types = ['jpg', 'jpeg',
                                       'png', ]
                    x = " , ".join(extension_types)
                    if not extention in extension_types:
                        message = {
                            'isError': True,
                            'title': "Validation Error",
                            'type': "warning",
                            'Message': f"This field only supports {x}"
                        }
                        return JsonResponse(message, status=200)

                    if file.size > 2621440:
                        message = {
                            'isError': True,
                            'title': "Limit Size!!!!",
                            'type': "warning",
                            'Message': file.name+'  file is more than 2mb size'
                        }
                        return JsonResponse(message, status=200)

                    # Validaet data
                    if first_name == '' or first_name == 'null' or first_name is None or first_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter first name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(first_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only  ' + first_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if father_name == '' or father_name == 'null' or father_name is None or father_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter father name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(father_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only first name ' + (father_name),
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if last_name == '' or last_name == 'null' or last_name is None or last_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter last name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(last_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only  ' + last_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if mother_name == '' or mother_name == 'null' or mother_name is None or mother_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an mother',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(mother_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only' + mother_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if gender == '' or gender == 'null' or gender is None or gender == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select gender',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if marital == '' or marital == 'null' or marital is None or marital == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select martial status',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Dob == '' or Dob == 'null' or Dob is None or Dob == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select date of birth',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    # print(Dob)
                    # if Dob > str(currentDate) :
                        
                    #     return JsonResponse(
                    #         {
                    #             'isError': True,
                    #             'Message': 'Please select valid date of birth',
                    #             'title': 'Validation Error!',
                    #             'type': 'warning',
                    #         }
                    #     )
                    # end = currentDate - timedelta(days=365*2)
                    # checkdob = difference_date(Dob, end)
                    # print(checkdob)
                    # if checkdob < 10:
                    #     return JsonResponse(
                    #         {
                    #             'isError': True,
                    #             'Message': 'This employee is younger then 2 years',
                    #             'title': 'Validation Error!',
                    #             'type': 'warning',
                    #         }
                    #     )
                    if phone == '' or phone == 'null' or phone is None or phone == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an phone number',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not phone_valid(phone):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid number like (252) 61 5 100 200  ' + (phone),
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if emergency_contect == '' or emergency_contect == 'null' or emergency_contect is None or emergency_contect == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an emergency contact  number',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if phone_valid(emergency_contect) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid emergency like 252 61 2323222  ' + emergency_contect,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if email == '' or email == 'null' or email is None or email == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an eamil',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if check(email) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid email like example@gmail.com',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if address == '' or address == 'null' or address is None or address == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an address',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validationNumber(address) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if speciality == '' or speciality == 'null' or speciality is None or speciality == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select title',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    first_name = RemoveSpecialCharacters(first_name)
                    father_name = RemoveSpecialCharacters(father_name)
                    last_name = RemoveSpecialCharacters(last_name)
                    mother_name = RemoveSpecialCharacters(mother_name)
                    address = RemoveSpecialCharacters(address)
                    email = RemoveSpecialCharacters(email)

                    is_email_exist = Employee.objects.filter(
                        email=email).exists()
                    if is_email_exist:
                        get_email_exist = Employee.objects.get(
                            email=email)
                        return JsonResponse(
                            {
                                'isError': True,
                                'title': 'Validation Error!',
                                'Message':       f' email-ka {email}  waxaa heysto shaqaaale  {get_email_exist.first_name} {get_email_exist.father_name}  {get_email_exist.last_name}',
                                'type': 'warning',
                            }
                        )

                    new_employee = Employee(emp_number=GenerateSerialNumber(), first_name=first_name, father_name=father_name, mother_name=mother_name, last_name=last_name, job_type_id=speciality, address=address, marital=marital,
                                            Blood_Group=Blood_Group, photo=file, emergency_contect=emergency_contect, dob=Dob, gender=gender,  email=email, phone=phone
                                            )
                    new_employee.save()
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "HR / Employee module"
                    action = f'{names} ayaa diwaan geliye shaqaale cusub oo magaciisu yahay {first_name} {father_name}  {last_name}'
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'new employee has been created',
                            'title': ' Successfully created!',
                            'type': 'success',

                        },
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to create employee',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )       
            if action == 'update_employee_data':
                if request.user.has_perm('Hr.change_employee'):
                    employee_id = request.POST.get('employee_id')
                    first_name = request.POST.get('first_name')
                    father_name = request.POST.get('father_name')
                    last_name = request.POST.get('last_name')
                    mother_name = request.POST.get('mother_name')
                    gender = request.POST.get('gender')
                    marital = request.POST.get(
                        'marital')  # this has problem
                    Dob = request.POST.get('Dob')
                    phone = request.POST.get('phone')
                    email = request.POST.get('email')
                    address = request.POST.get('address')
                    emergency_contect = request.POST.get(
                        'emergency_contect')
                    speciality = request.POST.get(
                        'speciality')  # this have problem
                    Blood_Group = request.POST.get('Blood_Group')

                    # Validaet data
                    if first_name == '' or first_name == 'null' or first_name is None or first_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter first name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(first_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only  ' + first_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if father_name == '' or father_name == 'null' or father_name is None or father_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter father name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(father_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only' + father_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if last_name == '' or last_name == 'null' or last_name is None or last_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter last name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(last_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only  ' + last_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if mother_name == '' or mother_name == 'null' or mother_name is None or mother_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an mother',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(mother_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a text only' + mother_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if gender == '' or gender == 'null' or gender is None or gender == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select gender',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if marital == '' or marital == 'null' or marital is None or marital == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select martial status',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Dob == '' or Dob == 'null' or Dob is None or Dob == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select date of birth',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if phone == '' or phone == 'null' or phone is None or phone == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an phone number',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if phone_valid(phone) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid number like 252 61 2323222  ' + phone,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if emergency_contect == '' or emergency_contect == 'null' or emergency_contect is None or emergency_contect == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an emergency contact  number',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if phone_valid(emergency_contect) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid emergency like 252 61 2323222  ' + emergency_contect,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if email == '' or email == 'null' or email is None or email == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an eamil',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if check(email) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter a valid email ' + email,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if address == '' or address == 'null' or address is None or address == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter an address',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validationNumber(address) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text or number with ,',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if speciality == '' or speciality == 'null' or speciality is None or speciality == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select title',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_employ_Detail = Employee.objects.get(
                        id=employee_id)
                    getspeciality = Title.objects.get(id=speciality)

                    first_name = RemoveSpecialCharacters(first_name)
                    father_name = RemoveSpecialCharacters(father_name)
                    last_name = RemoveSpecialCharacters(last_name)
                    mother_name = RemoveSpecialCharacters(mother_name)
                    address = RemoveSpecialCharacters(address)
                    email = RemoveSpecialCharacters(email)

                    update_employ_Detail.first_name = first_name
                    update_employ_Detail.father_name = father_name
                    update_employ_Detail.last_name = last_name
                    update_employ_Detail.mother_name = mother_name
                    update_employ_Detail.Blood_Group = Blood_Group
                    update_employ_Detail.dob = Dob
                    update_employ_Detail.gender = gender
                    update_employ_Detail.phone = phone
                    update_employ_Detail.emergency_contect = emergency_contect
                    update_employ_Detail.email = email
                    update_employ_Detail.address = address
                    update_employ_Detail.marital = marital
                    update_employ_Detail.job_type = getspeciality
                    update_employ_Detail.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': update_employ_Detail.get_full_name() + '  updated',
                            'title': 'Successfully Updated !' ,
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to edit employee ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                    )
            if action == "getEmployeeData":
                if request.user.has_perm('Hr.view_employee'):
                    id = request.POST.get('employee_id')

                    getemployee_id = Employee.objects.get(id=id)

                    message = {
                        'id': getemployee_id.id,
                        'employee_firstname': getemployee_id.first_name,
                        'employee_father_name': getemployee_id.father_name,
                        'employee_last_name': getemployee_id.last_name,
                        'employee_mother_name': getemployee_id.mother_name,
                        'dob': getemployee_id.dob,
                        'email': getemployee_id.email,
                        'gender': getemployee_id.gender,
                        'phone': getemployee_id.phone,
                        'emergency_contact': getemployee_id.emergency_contect,
                        'maritial': getemployee_id.marital,
                        'address': getemployee_id.address,
                        'blood_group': getemployee_id.Blood_Group,
                        'date_join': getemployee_id.created,
                        'title': getemployee_id.job_type.id,
                        'titlename': getemployee_id.job_type.name
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to see employee ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                    )
            if action == "getAllEmployeData":  
                if request.user.has_perm('Hr.view_employee'):   
                    id = request.POST.get('id')
                    employesingledata = Employee.objects.get(
                        id=id)
                    

                    message = []
                    message = {
                        'id': employesingledata.id,
                        'first_name': employesingledata.first_name,
                        'fullname': employesingledata.get_full_name(),
                        'father_name': employesingledata.father_name,
                        'last_name': employesingledata.last_name,
                        'mother_name': employesingledata.mother_name,
                        'dob': employesingledata.dob,
                        'd_Phone': employesingledata.phone,
                        'email': employesingledata.email,
                        'address': employesingledata.address,
                        'gender': employesingledata.gender,
                        'maritial': employesingledata.marital,
                        'Emargency_contact': employesingledata.emergency_contect,
                        'blood_group': employesingledata.Blood_Group,
                        'title': employesingledata.job_type.id,
                        'titlename': employesingledata.job_type.name,

                        'date_join': employesingledata.created,
                        'emp_approve': employesingledata.Employee_state,





                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to see employee ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                    )
            if action == 'update_profile_picture':
                if request.user.has_perm('Hr.change_employee'):
                    id = request.POST.get('employee_id')
                    try:
                        file = request.FILES['image']
                    except KeyError:
                        file = None
                    if file is None or file == '':
                        message = {
                            'isError': True,
                            'title': "Validation Error",
                            'type': "warning",
                            'Message': 'Please upload photo.'
                        }
                        return JsonResponse(message, status=200)

                    extention = file.name.split(".")[-1]
                    extention = extention.lower()
                    extension_types = ['jpg', 'jpeg',
                                        'png', 'pdf', 'txt', ]
                    x = " , ".join(extension_types)
                    if not extention in extension_types:
                        message = {
                            'isError': True,
                            'title': "Validation Error",
                            'type': "warning",
                            'Message': f"This field only supports {x}"
                        }
                        return JsonResponse(message, status=200)

                    if file.size > 2621440:
                        message = {
                            'isError': True,
                            'title': "Limit Size!!!!",
                            'type': "warning",
                            'Message': file.name+'  file is more than 2mb size'
                        }
                        return JsonResponse(message, status=200)

                    update_empl_photo = Employee.objects.get(
                        id=id)
                    update_empl_photo.photo = file
                    update_empl_photo.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'Documents  has been updated',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You Dont have permission to change to profile ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                    )
            if action == 'approve_reject_employee':
                if request.user.has_perm('Hr.Approve_employee'):
                    # Get all data from the request

                    employee_id = request.POST.get('employee_id')
                    status = request.POST.get('status')

                    # Validaet data

                    if status == '' or status == 'null' or status is None or status == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose State',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if employee_id == '' or employee_id == 'null' or employee_id is None or employee_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose State',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_employ_state = Employee.objects.get(
                        id=employee_id)
                    update_employ_state.Employee_state = status
                    update_employ_state.appprovedwho = request.user.username

                    update_employ_state.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': '  updated',
                            'title':  " has been successfully ",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'You dont have permission to approve or reject',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    },
                      )
            if action == "getemployeePresentdata":  
                if request.user.has_perm('Hr.view_attandence'):
                    id = request.POST.get('id')              
                    getAttendance = Attandence.objects.filter(
                        employee_id=id ,state = "1")
                    message = []
                    for xattendance in range(0, len(getAttendance)):
                        date_str = getAttendance[xattendance].today_date # input date as a string,                    
                        day_name = date_str.strftime("%A")  # get the day name from the datetime object
                        message.append({
                            'id': getAttendance[xattendance].id,                            
                            'employeeName': getAttendance[xattendance].employee.get_full_name(),                            
                            'shift_name': getAttendance[xattendance].shift.shift_name,
                            'shift_type': getAttendance[xattendance].shift.shift_type,
                            'shift_start': getAttendance[xattendance].shift.start_time,
                            'end_shift': getAttendance[xattendance].shift.end_time,                   
                            'stateday': getAttendance[xattendance].today_date,
                            'state':'Present' if getAttendance[xattendance].state == "1" else "Absent",
                            'dayname': day_name,

                           

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if action == "getemployeAbsentdata":  
                            if request.user.has_perm('Hr.view_attandence'):
                                id = request.POST.get('id')              
                                getAttendance = Attandence.objects.filter(
                                    employee_id=id ,state = "0")
                                message = []
                                for xattendance in range(0, len(getAttendance)):
                                    date_str = getAttendance[xattendance].today_date # input date as a string,                    
                                    day_name = date_str.strftime("%A")  # get the day name from the datetime object
                                    message.append({
                                        'id': getAttendance[xattendance].id,                            
                                        'employeeName': getAttendance[xattendance].employee.get_full_name(),                            
                                        'shift_name': getAttendance[xattendance].shift.shift_name,
                                        'shift_type': getAttendance[xattendance].shift.shift_type,
                                        'shift_start': getAttendance[xattendance].shift.start_time,
                                        'end_shift': getAttendance[xattendance].shift.end_time,                   
                                        'stateday': getAttendance[xattendance].today_date,
                                        'state':'Present' if getAttendance[xattendance].state == "1" else "Absent",
                                        'dayname': day_name,

                                    

                                    })
                                return JsonResponse({'isError': False, 'Message': message}, status=200)
                            else:
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Access is Denied! ',
                                    'title': 'No Access Permission',
                                    'type': 'warning',

                                })
            if action == "getleaveHistory":  
                if request.user.has_perm('Hr.view_attandence'):
                    id = request.POST.get('id')              
                    getLeaveHistory = Employee_Leave.objects.filter(
                        employee_id=id , State = "Confirmed")
                    message = []
                    for xleaveHistory in range(0, len(getLeaveHistory)): 
                        total =   getLeaveHistory[xleaveHistory].endtday - currentDate                      
                        if currentDate == getLeaveHistory[xleaveHistory].endtday:
                            total = 'Completed '
                        elif currentDate > getLeaveHistory[xleaveHistory].endtday:
                            total = 'Completed '
                        else:
                            total = get_modified_date(total)
                      

                        message.append({
                            'id': getLeaveHistory[xleaveHistory].id,                            
                            'leaveType': getLeaveHistory[xleaveHistory].leave_ct.name,                            
                            'leaveTypenumber': getLeaveHistory[xleaveHistory].leave_ct.n_days,                            
                            'remaindays': total,                            
                            'startDay': getLeaveHistory[xleaveHistory].startday,                            
                            'Endday': getLeaveHistory[xleaveHistory].endtday,                            
                            'leaveState': getLeaveHistory[xleaveHistory].State,                            
                            'approvedWho': 'not approved yet' if  getLeaveHistory[xleaveHistory].approvedBy is None else getLeaveHistory[xleaveHistory].approvedBy,                            
                            
                           

                        

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            
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

def printEmployeeData(request):
    try:
        input = request.GET['inputs']
        employeid = request.GET['employee']   

        if ',' in input:
            input = input.split(',')
        else:
            input[input]

        expected = ['basicInfo', 'Qualification', 'Experience', 'Job', 'Accounts']

        clearfield = []

        basic_info = ''
        qualification = ''
        experiences = ''
        job_details = ''
        Accounts = ''


        for index, item in enumerate(input):
            if item in expected:
                clearfield.append(item)

        if  'basicInfo' in clearfield:
            basic_info = Employee.objects.get(id = employeid)

        if  'Qualification' in clearfield:
            qualification = Qualification.objects.filter(employee_id = employeid)

          
        if  'Experience' in clearfield:
            experiences = Experience.objects.filter(employee_id = employeid)

        if  'Job' in clearfield:
            job_details = JobDetails.objects.filter(employee_id = employeid, is_active = True ,job_state = "Approved")
           
        
        if  'Accounts' in clearfield:
            Accounts = EmployeeBank.objects.filter(employee_id = employeid)
 
        print(job_details,'waa job detail an wado')
        context = {
            'isError': False,
            'pk':employeid,
            'basic_info': basic_info,
            'qualification':qualification ,
            'experiences': experiences,
            'jobs_details': job_details,
            'Accounts': Accounts,
        }
        return render(request, 'Hr/printEmployeDetail.html',context)
    
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/500.html', context)