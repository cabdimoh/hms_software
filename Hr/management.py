from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from .views import *
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re
from datetime import date
currentDate = datetime.date.today()


@login_required(login_url='Login')
def departments(request):
    try:
        if request.user.has_perm('Hr.view_jobdetails'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'depName' in request.GET
            Jobtitle = 'All'
            DataNumber = 30
            SearchQuery = ''
            EmployeeList = []

            if Checkjobtitle:
                Jobtitle = request.GET['depName']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['department_all__id'] = Jobtitle

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = JobDetails.objects.filter(
                    Q(employee_type__icontains=SearchQuery) |
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__father_name__icontains=SearchQuery) |
                    Q(employee__last_name__icontains=SearchQuery) |
                    Q(depar_section__department_sections__icontains=SearchQuery),
                    ~Q(employee_type__icontains="General-Director"),
                    ~Q(employee_type__icontains="Director-Secretory"),
                    **dataFiltering,
                    employee__is_terminated=False,
                    is_active=True,
                    job_state="Approved",





                )
            else:
                EmployeeList = JobDetails.objects.filter(
                    ~Q(employee_type__icontains="General-Director"),
                    ~Q(employee_type__icontains="Director-Secretory"),
                    **dataFiltering, is_active=True,  employee__is_terminated=False, job_state="Approved", )

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
                'depName': Jobtitle,
                'pageTitle': 'Employee List',
                'deparments': Departments.objects.all(),
                'sections': Depart_Sections.objects.all(),

            }
            return render(request, 'Hr/Management/Departments.html', context)
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
def Management_setup(request):
    try:
        if request.user.has_perm('Hr.Approve_employee'):
            context = {
                'department_all': Departments.objects.all(),
                'all_jobtypes': JobType.objects.all(),
                'departments': Departments.objects.all(),
                'directarate_all': Directorate.objects.all(),
            }
            return render(request, 'Hr/Management/manage_sutup.html', context)
        else:
            return render(request, 'Hr/403.html', )

    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'Hr/Management/manage_sutup.html', context)

@login_required(login_url='Login')
def SearchEmployee(request):
    search = request.POST.get('employee')
    if request.method == 'POST':
        searchQuery = JobDetails.objects.filter(
            Q(employee__emp_number__icontains=search) |
            Q(employee__email__icontains=search) |
            Q(employee__phone__icontains=search) |
            Q(employee__first_name__icontains=search) |
            Q(employee__last_name__icontains=search) |
            Q(employee__father_name__icontains=search),
            ~Q(employee_type__icontains="General-Director"),
            ~Q(employee_type__icontains="Director-Secretory"),
            ~Q(employee_type__icontains="Department-Head"),
            employee__is_terminated=False,
            job_state="Approved",
            is_active=True


        )

        message = []

        for xSearch in range(0, len(searchQuery)):

            message.append({
                'label': f"{searchQuery[xSearch].employee.emp_number} - {searchQuery[xSearch].employee.get_full_name()}  ",
                'userid': searchQuery[xSearch].employee.id,
            },
            )
        return JsonResponse({'Message': message}, status=200)

# Attandence
@login_required(login_url='Login')
def attendance(request):
    try:
        if request.user.has_perm('Hr.view_attandence'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET           
            CheckdepName = 'depName' in request.GET            
            depName = 'All'          
            DataNumber = 30
            SearchQuery = ''            
            day_names = currentDate.strftime("%A") 
            manageshiftlist = []
            if CheckdepName:
                depName = request.GET['depName']

            dataFiltering = {}
            if depName != 'All':
                dataFiltering["shift__department__id"] = depName
                
            getattendid = Attandence.objects.filter( **dataFiltering,   today_date=currentDate).values('employee').distinct()
            is_attended_today = Attandence.objects.filter( **dataFiltering,   today_date=currentDate).exists()

            if is_attended_today:                
                filter = Q(employee__in = getattendid)
            else:
                filter = ~Q(employee__in = getattendid)


            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])
            get_data=[]
            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                manageshiftlist = Manage_shift.objects.filter(
                    Q(employee__first_name__icontains=SearchQuery)  |   
                    Q(employee__father_name__icontains=SearchQuery)  |
                    Q(employee__last_name__icontains=SearchQuery)  ,   
                    filter,
                    **dataFiltering,                          
                )
                
            else:                             
                getattenditoday = Manage_shift.objects.all()
                for i in getattenditoday:
                    shiftdays = i.shift.shift_date
                    shiftdays = shiftdays.split(',') 
                    for d in shiftdays:                      
                       if day_names == d:
                            i.existday = True                      
                            i.save()   
                            break                    
                       else:
                            i.existday = False                      
                            i.save()  
                           


                manageshiftlist = Manage_shift.objects.filter(
                     filter,
                    **dataFiltering,
                      existday = True
                  ).order_by('employee__emp_number')
            if len(manageshiftlist) > 0:
                get_data=manageshiftlist[0]
            else:
                get_data
            paginator = Paginator(manageshiftlist, DataNumber,)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'depName': depName,
                'pageTitle': 'Employee List',
                'job_types': Title.objects.all(),
                'departlist': Departments.objects.all(),
                'get_data':get_data,
                'day_name':day_names,

       



            }
            return render(request, 'Hr/Management/attandence.html', context)
        return render(request, 'Hr/403.html', )

    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request,'Hr/500.html',context)


@login_required(login_url='Login')
def attendanceAction(request):
    try:
        if request.user.has_perm('Hr.view_attandence'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkdep = 'depName' in request.GET   
            Checkdate = 'datechoose' in request.GET   
            Checkattendings = 'attendings' in request.GET 
            type_post = 'All' 
            DataNumber = 5
            depName = 'All'
            datechoose = currentDate.strftime('%Y-%m-%d')
            SearchQuery = ''
            shifts = []
            # get_shift_info= Work_shift.objects.get(id=id)
           

            if Checkattendings:
                type_post = request.GET['attendings']


            if Checkdate:
                datechoose = request.GET['datechoose']

                expand = [int(x) for x in datechoose.split('-')]
                datechoose = date(expand[0] , expand[1] , expand[2]).strftime('%Y-%m-%d')
                


            if Checkdep:
                depName = request.GET['depName']
              

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

           
            today = date.today()
            day_name = today.strftime("%A")

            datafiltering = {}
            if type_post != 'All':
               datafiltering['state'] = type_post
            
            if depName != 'All':
               datafiltering['shift__department__id'] = depName
                
            
            employe_shift = Manage_shift.objects.all().values('employee').distinct()



                       
               
            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                shifts = Attandence.objects.filter(
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__emp_number__icontains=SearchQuery),
                    **datafiltering,
                      today_date = datechoose,
                ).order_by('employee__emp_number')
            else:
               
                shifts = Attandence.objects.filter(                   
                **datafiltering,
                  today_date = datechoose,
                 
                
                # shift_id____department= depName

                    

                ).order_by('id',)

              
            

                

            paginator = Paginator(shifts, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,              
                'depName':depName,
                'attendings':type_post,
                'pageTitle': 'Employee List',
                'department_all': Departments.objects.all(),
                'workshifts': Work_shift.objects.all(),
                'day_name':day_name,
                'datechoose':datechoose,
                # 'get_shift':get_shift_info,
                # 'type':type_post





            }
            return render(request, 'Hr/Management/AttendanceAction.html',context)


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
        return render(request, 'Hr/500.html',context)

def manage_Attendance(request, activity):
    try:
        if request.method == "POST":
            if activity == "take_attendance":
                if request.user.has_perm('Hr.add_attandence'):
                    employe = request.POST.get('employees')                    
                    shiftid = request.POST.get('shift')
                    status = request.POST.get('status')
                    department=request.POST.get('department')
                    if employe == '' or employe == 'null' or employe is None or employe == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'check or uncheck employee',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if department == '' or department == 'null' or department is None or department == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'PLease select Department',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                  
                    if ',' in status:
                        status=status.split(',')
                    else:
                        status=[status]

                    if ',' in employe:
                        employe=employe.split(',')
                    else:
                        employe=[employe]

                    if ',' in shiftid:
                        shiftid=shiftid.split(',')
                    else:
                        shiftid=[shiftid]
                    status_state=''
                   

                    # getting employees deparment 
                    # get_emp_dept = Manage_shift.objects.filter(shift__department=department).values('employee')       
                    for xrow in range(0,len(employe)):
                        if  status[xrow] == '':
                            status_state= '0'
                        else:
                            status_state=status[xrow] 
                        
                        setemploye = Attandence(
                                employee_id = employe[xrow], shift_id = shiftid[xrow],today_date = currentDate, state = status_state
                                )
                        setemploye.save()                   
                    return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'New attendance is been taken',
                                'title': 'Successfully!',
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to add employee attendance',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if activity == "update_attendance":
                if request.user.has_perm('Hr.change_attandence'):
                    employe = request.POST.get('employees')                    
                    shiftid = request.POST.get('shift')
                    status = request.POST.get('status')
                    attendID = request.POST.get('attendID')
                    
                    if employe == '' or employe == 'null' or employe is None or employe == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'check or uncheck employee',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if ',' in status:
                        status=status.split(',')
                    else:
                        status=[status]

                    if ',' in employe:
                        employe=employe.split(',')
                    else:
                        employe=[employe]
                    if ',' in shiftid:
                        shiftid=shiftid.split(',')
                    else:
                        shiftid=[shiftid]

                    if ',' in attendID:
                        attendID=attendID.split(',')
                    else:
                        attendID=[attendID]

                    for xrow in range(0,len(employe)):
                        get_attendace=Attandence.objects.get(id=attendID[xrow])
                        get_attendace.employee_id = employe[xrow]
                        get_attendace.shift_id = shiftid[xrow]
                        get_attendace.today_date = currentDate
                        get_attendace.state = status[xrow]
                        get_attendace.save()
                    return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'Attendance has been successfully updated',
                                'title': 'Successfully!',
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to change employee attendance',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if activity == "get_single_shiftmanagement":
                id = request.POST.get('id')

                all_shifts = Manage_shift.objects.filter(id=id)
                message = []
                for xshifts in range(0, len(all_shifts)):
                    message.append({

                        'id': all_shifts[xshifts].id,
                        'days': all_shifts[xshifts].shift.shift_date,


                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            if activity == "get_attending_days":
                id = request.POST.get('id')
                getalldays = Attandence.objects.all().values('shift__shift_date')
              
                all_shifts = Attandence.objects.filter(id=id)
                message = []
                for xshifts in range(0, len(all_shifts)):
                    message.append({

                        'id': all_shifts[xshifts].id,
                        'days': all_shifts[xshifts].shift.shift_date


                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return JsonResponse(
            {
                'isError': True,
                'Message': f'{error}',
                'title': f'On Error Occurs',
                'type': 'warning',

            },
        )

@login_required(login_url='Login')
def view_shift(request, id):
    try:
        if request.user.has_perm('Hr.view_manage_shift'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'depName' in request.GET       
            type_post = 'shifted'          
            DataNumber = 30
            SearchQuery = ''
            shifts = []    
            get_shift_info= Work_shift.objects.get(id=id)            
            if Checkjobtitle:
                type_post = request.GET['depName']
              

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            shifted_employees = Manage_shift.objects.all().values('employee').distinct()     
            shiftedAttendid = Manage_shift.objects.filter(shift_id = id).values('employee').distinct()     

            if type_post == 'unshifted':
                filters = ~Q(employee__in = shifted_employees)
               
            else:
                filters = Q(employee__in = shifted_employees) 
                filters = Q(employee__in = shiftedAttendid) 
                

               

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                shifts = JobDetails.objects.filter(
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__father_name__icontains=SearchQuery) |
                    Q(employee__last_name__icontains=SearchQuery) |
                    Q(department_all__department_name__icontains=SearchQuery) |
                    Q(depar_section__department_sections__icontains=SearchQuery),                  
                    ~Q(employee_type__icontains="General-Director"),
                    ~Q(employee_type__icontains="Director-Secretory"),
                    ~Q(employee_type__icontains="Department-Head"),
                    filters,
                    employee__is_terminated=False,
                    is_active=True,
                    job_state="Approved",
                     department_all=get_shift_info.department
                    




                )
            else:
                shifts = JobDetails.objects.filter(
                    ~Q(employee_type__icontains="General-Director"),
                    ~Q(employee_type__icontains="Director-Secretory"),
                    ~Q(employee_type__icontains="Department-Head"),
                    filters,                 
                    employee__is_terminated=False,
                    is_active=True,
                    job_state="Approved",
                     department_all = get_shift_info.department

                )

            paginator = Paginator(shifts, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'depName': type_post,
                'pageTitle': 'Employee List',
                'department_all': Departments.objects.all(),
                'workshifts': Work_shift.objects.all(),
                'get_shift':get_shift_info,
                'type':type_post





            }
            return render(request, 'Hr/Management/manage_shift.html', context)
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
def CreateShift(request):
    try:
        context = {
            "department_all": Departments.objects.all()
        }
        return render(request, 'Hr/Management/shifts.html', context)

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
def management_shift(request, activity):
    try:
        if request.method == "POST":
            if activity == "new_assigning_shift":
                if request.user.has_perm('Hr.add_manage_shift'):
                    employe = request.POST.get('employees')
                    shiftid = request.POST.get('shift')
                    status = request.POST.get('status')                  
                    if employe == '' or employe == 'null' or employe is None or employe == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'check or uncheck employee',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if status == '' or status == 'null' or status is None or status == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'what status is',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if status == 'Approved':
                        all_employe_id = employe.split(',')
                        for id in all_employe_id:
                            if Manage_shift.objects.filter(employee_id=id).exists():
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'all existed in the shift list',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )

                            else:
                                setemploye = Manage_shift(
                                    shift_id=shiftid, employee_id=id, state="active")
                                setemploye.save()
                        return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'New shift  has been created',
                                'title': 'Successfull!',
                                'type': 'success',
                            }
                        )
                    else:
                        all_employe_id = employe.split(',')
                        for id in all_employe_id:
                            remshift = Manage_shift.objects.filter(employee_id=id ,shift_id = shiftid)                            
                            remshift.delete()
                            if Attandence.objects.filter(employee = id, today_date = currentDate , shift_id = shiftid).exists():
                                remattend=Attandence.objects.filter(employee = id, today_date = currentDate , shift_id = shiftid)
                                remattend.delete()
                            else:
                                return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'selected employee not belong to this shift',
                                'title': ' Not Shifted!',
                                'type': 'warning',
                            }
                        )

                        return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'select employee shift  has been deleted',
                                'title': 'Successfull Deleted!',
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to add employee shift',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if activity == "get_employee_department":

                employeeid = request.POST.get('employee_id')

                all_specialization = JobDetails.objects.filter(
                    employee__id=employeeid)
                message = []
                for xspecilization in range(0, len(all_specialization)):
                    message.append({

                        'Jobid': all_specialization[xspecilization].id,
                        'id': all_specialization[xspecilization].department_all.id,
                        'name': all_specialization[xspecilization].department_all.department_name,


                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            if activity == "get_department_shift":

                departid = request.POST.get('depart_id')

                all_shifts = Work_shift.objects.filter(department__id=departid)
                message = []
                for xshifts in range(0, len(all_shifts)):
                    message.append({

                        'id': all_shifts[xshifts].id,
                        'name': all_shifts[xshifts].shift_name,


                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)

    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return JsonResponse(
            {
                'isError': True,
                'Message': f'{error}',
                'title': f'On Error Occurs',
                'type': 'warning',

            },
        )



