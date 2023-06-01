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

@login_required(login_url='Login')
def viewExitCotegroy(request):
    try:
        if request.user.has_perm('Hr.view_employee_exit_category'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee_exit_Category.objects.filter(
                    Q(category_name__icontains=SearchQuery) |
                    Q(id__icontains=SearchQuery)





                )
            else:
                EmployeeList = Employee_exit_Category.objects.all()

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',





            }
            return render(request, 'Hr/exitCotegory.html', context)

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
        return render(request, 'Hr/500.html')

@login_required(login_url='Login')
def manage_exit_cotegory(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_Category':
                if request.user.has_perm('Hr.add_employee_exit_category'):    
                    Exit_Cotegory_name = request.POST.get('Exit_Cotegory_name')
                    if Exit_Cotegory_name == '' or Exit_Cotegory_name == 'null' or Exit_Cotegory_name is None or Exit_Cotegory_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter cotegory name' + Exit_Cotegory_name + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if text_validation(Exit_Cotegory_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only cotegory ' + Exit_Cotegory_name + " ",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    job_type = Employee_exit_Category(
                        category_name=Exit_Cotegory_name)
                    job_type.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new exit called {Exit_Cotegory_name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
        if activity == "get_exit_cotegory":
            if request.method == 'POST':
                
                single_exit_cotegory = Employee_exit_Category.objects.all()
                message = []
                for xcotegory in range(0, len(single_exit_cotegory)):
                    message.append({
                        'id': single_exit_cotegory[xcotegory].id,
                        'category_name': single_exit_cotegory[xcotegory].category_name,


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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)


# employee termination
@login_required(login_url='Login')
def view_Exit_Employe(request):
    try:

        if request.user.has_perm('Hr.view_exited_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = exited_employee.objects.filter(
                    Q(exit_emp__first_name__icontains=SearchQuery) |
                    Q(exit_emp__father_name__icontains=SearchQuery) |
                    Q(exit_emp__last_name__icontains=SearchQuery) |
                    Q(exit_emp_category__category_name__icontains=SearchQuery) |
                    Q(id__icontains=SearchQuery)





                )
            else:
                EmployeeList = exited_employee.objects.all()

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',
                'exit_cotegory': Employee_exit_Category.objects.all(),
                'employee_list': Employee.objects.filter(is_terminated=False)





            }
            return render(request, 'Hr/exitEmployee.html', context)
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
def manage_exit_employee(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_exit_employee':
                if request.user.has_perm('Hr.add_exited_employee'):
                    try:
                        file = request.FILES['documents']
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
                                    'pdf', 'txt', ]
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

                    exited_employee_id = request.POST.get('userIDs')
                    exit_cotegory_id = request.POST.get('exit_cotegory_id')
                    exit_reason = request.POST.get('exit_reason')
                    date_death = request.POST.get('date_death')
                    time_death = request.POST.get('time_death')

                    if exited_employee_id == '' or exited_employee_id == 'null' or exited_employee_id is None or exited_employee_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Employee name' + exited_employee_id + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if exit_cotegory_id == '' or exit_cotegory_id == 'null' or exit_cotegory_id is None or exit_cotegory_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter exit category name' + exit_cotegory_id + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if exit_reason == '' or exit_reason == 'null' or exit_reason is None or exit_reason == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter reason' + exit_reason + " is removing",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    get_employe = Employee.objects.get(id=exited_employee_id)

                    if exited_employee.objects.filter(exit_emp=exited_employee_id).exists():
                        return JsonResponse(

                            {
                                'isError': True,
                                'Message':  get_employe.get_full_name() + " already exits",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if get_employe.Employee_state == "Pending" or get_employe.Employee_state == "Rejected":
                        return JsonResponse(

                            {
                                'isError': True,
                                'Message':  get_employe.get_full_name() + " is Pending or Reject State",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    get_exit_cotegory = Employee_exit_Category.objects.get(
                        id=exit_cotegory_id)

                    if (get_exit_cotegory.category_name).lower() == "death":
                        if date_death == '' or time_death == '':

                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter death date and time of death'  "",
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                       
                    else:
                        date_death = None
                        time_death = None
                    exit_reason = RemoveSpecialCharacters(exit_reason)
                    exit_employe_save = exited_employee(
                        exit_emp=get_employe, exit_emp_category=get_exit_cotegory, reason=exit_reason, document=file, dayHappen=date_death, timeHappen=time_death)
                    exit_employe_save.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New exited has been created',
                            'title': 'Successfully ',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Dont have permission to add employee exit ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })        
            if activity == "get_exit_employee": 
                if request.user.has_perm('Hr.view_exited_employee'):
                    single_exit_cotegory = exited_employee.objects.all()
                    message = []
                    for xcotegory in range(0, len(single_exit_cotegory)):
                        message.append({
                            'id': single_exit_cotegory[xcotegory].id,
                            'employee_name': single_exit_cotegory[xcotegory].exit_emp.get_full_name,
                            'category_name': single_exit_cotegory[xcotegory].exit_emp_category.category_name,


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
            if activity == "get_exit_detail":
                if request.user.has_perm('Hr.view_exited_employee'):
                    id = request.POST.get('id')              
                    getexisteempl = exited_employee.objects.filter(
                        id=id)
                    message = []
                    for xexited in range(0, len(getexisteempl)):
                        message.append({
                            'id': getexisteempl[xexited].id,
                            'employe_name': getexisteempl[xexited].exit_emp.get_full_name(),
                            'category': getexisteempl[xexited].exit_emp_category.id,
                            'reason': getexisteempl[xexited].reason,
                            'dayhappen': getexisteempl[xexited].dayHappen,
                            'timeHappen': getexisteempl[xexited].timeHappen, 
                            'approvedWho':"not Approved yet" if getexisteempl[xexited].appprovedwho is None else 'somalia',                         

                            'exitstate': getexisteempl[xexited].exit_state,                       
                            'Created': getexisteempl[xexited].date_format(),                       

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Dont have permission to view employee exit ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })  
            if activity == 'approve_reject_exit':
                if request.user.has_perm('Hr.Approve_employee'):
                    # Get all data from the request

                    ID = request.POST.get('ID')
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

                    if ID == '' or ID == 'null' or ID is None or ID == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose State',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if status == 'Confirmed':
                    
                        exitedState = exited_employee.objects.get(id=ID)
                        exitedState.exit_state = status
                        exitedState.appprovedwho = request.user.username
                        exitedState.save()

                        employee_id = exitedState.exit_emp                  
                        employee_id.is_terminated = True
                    
                        employee_id.save()

                        return JsonResponse(
                            {
                                'isError': False,
                                'Message': '  updated',
                                'title':  " has been successfully ",
                                'type': 'success',
                            }
                        )

                    if status == 'Returned':
                        print(status + ' ayan wadaa')
                        if exited_employee.objects.filter(id=ID).exists():
                            exitedState = exited_employee.objects.get(id=ID)
                            exitedState.exit_emp.is_terminated = True
                            exitedState.exit_state = status
                            exitedState.appprovedwho = request.user.username
                            exitedState.save()

                            employee_id = exitedState.exit_emp
                            print(f"Employee {employee_id}")
                            employee_id.is_terminated = False
                            employee_id.Employee_state = "Pending"
                            employee_id.save()
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
                                    'Message': 'this exited is not exist check your previous exited employee',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if status == 'Rejected':
                        print(status + 'ayan wadaa')
                        if exited_employee.objects.filter(id=ID).exists():
                            exitedState = exited_employee.objects.get(id=ID)
                            exitedState.delete()
                            return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'this exited is been deleted',
                                    'title':  " has been successfully ",
                                    'type': 'success',
                                }
                            )
                        else:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'this exited is not exist check your previous exited employee',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if activity == "get_employee_name":
                
                    employee_id = request.POST.get('employee_id')

                    all_specialization = Employee.objects.filter(id=employee_id)
                    message = []
                    for xspecilization in range(0, len(all_specialization)):
                        message.append({

                            'id': all_specialization[xspecilization].id,
                            'fullname': all_specialization[xspecilization].first_name,


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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)

@login_required(login_url='Login')
def view_Death_Employe(request):
    try:

        if request.user.has_perm('Hr.view_exited_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = exited_employee.objects.filter(
                    Q(exit_emp__first_name__icontains=SearchQuery) |
                    Q(exit_emp__father_name__icontains=SearchQuery) |
                    Q(exit_emp__last_name__icontains=SearchQuery) |
                    Q(exit_emp_category__category_name__icontains=SearchQuery) |
                    Q(id__icontains=SearchQuery), exit_emp_category__category_name='Death'





                )
            else:
                EmployeeList = exited_employee.objects.filter(
                    exit_emp_category__category_name='Death'
                )

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',
                'exit_cotegory': Employee_exit_Category.objects.all(),
                'employee_list': Employee.objects.filter(is_terminated=False)





            }
            return render(request, 'Hr/DeathEmployee.html', context)

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

# employee termination catogory
@login_required(login_url='Login')
def viewLeaveCotegroy(request):
    try:
        if request.user.has_perm('Hr.view_employee_exit_category'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 5
            SearchQuery = ''
            EmployeeList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = LeaveCatogory.objects.filter(
                    Q(id__icontains=SearchQuery)|
                    Q(name__icontains=SearchQuery) 





                )
            else:
                EmployeeList = LeaveCatogory.objects.all()

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',





            }
            return render(request, 'Hr/LeaveCategory.html', context)

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


@login_required(login_url='Login')
def manage_Leave_cotegory(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_leave_Category':
                # if request.user.has_perm('Hr.add_employee_exit_category'):    
                    name = request.POST.get('name')
                    leave_days = request.POST.get('leavedays')
                    if name == '' or name == 'null' or name is None or name == 'undefined': 
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter cotegory name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if leave_days == '' or leave_days == 'null' or leave_days is None or leave_days == 'undefined': 
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': f'Please enter number of {name} days',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only cotegory ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    leavesave = LeaveCatogory(
                        name=name, n_days = leave_days)
                    leavesave.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new Leave category called {name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                # else:
                #     return JsonResponse(
                #     {
                #         'isError': True,
                #         'Message': 'Access is Denied! ',
                #         'title': 'No Access Permission',
                #         'type': 'warning',

                #     })
                
            if activity == 'update_leave_Category':
                # if request.user.has_perm('Hr.add_employee_exit_category'):    
                    id = request.POST.get('id')
                    name = request.POST.get('name')
                    leave_days = request.POST.get('leavedays')
                    if leave_days == '' or leave_days == 'null' or leave_days is None or leave_days == 'undefined': 
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': f'Please enter number of {name} days',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if name == '' or name == 'null' or name is None or name == 'undefined': 
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter cotegory name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only cotegory ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    leavesave = LeaveCatogory.objects.get(id = id )
                    leavesave.name = name
                    leavesave.n_days = leave_days
                    leavesave.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'Leave category called {name}  has been updated',
                            'title': 'successfully updated !',
                            'type': 'success',
                        }
                    )
                # else:
                #     return JsonResponse(
                #     {
                #         'isError': True,
                #         'Message': 'Access is Denied! ',
                #         'title': 'No Access Permission',
                #         'type': 'warning',
                #     })
                
            if activity == "get_leave_Category":  
                id = request.POST.get('id')    
                leavCat = LeaveCatogory.objects.filter  (id = id)
                message = []
                for xcotegory in range(0, len(leavCat)):
                    message.append({
                        'id': leavCat[xcotegory].id,
                        'name': leavCat[xcotegory].name,
                        'day': leavCat[xcotegory].n_days,
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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)


# employee termination
@login_required(login_url='Login')
def view_Leave_Employe(request):
    try:
        # if request.user.has_perm('Hr.view_exited_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            checkdepartment = 'departmentN' in request.GET
            DataNumber = 5
            departmentN = 'All'
            SearchQuery = ''
            EmployeeList = []
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])


            dataFiltering = {}
            if checkdepartment:
                departmentN = request.GET['departmentN']

            if departmentN != "All":
                dataFiltering['department_all_id'] = departmentN

            getattendid = JobDetails.objects.filter(**dataFiltering ,is_active = True).values('employee').distinct()

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = Employee_Leave.objects.filter(
                    Q(employee__in = getattendid)

                    # Q(exit_emp__first_name__icontains=SearchQuery) |
                    # Q(exit_emp__father_name__icontains=SearchQuery) |
                    # Q(exit_emp__last_name__icontains=SearchQuery) |
                    # Q(exit_emp_category__category_name__icontains=SearchQuery) |
                    # Q(id__icontains=SearchQuery)

                    )
            else:
                EmployeeList = Employee_Leave.objects.filter(
                    Q(employee__in = getattendid)
                            )

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',
                'leave_cotegory': LeaveCatogory.objects.all(),
                'Departments_all': Departments.objects.all(),
                'employee_list': Employee.objects.filter(is_terminated=False),
                'departmentN': departmentN,
                
                
            }
            return render(request, 'Hr/leaveEmployee.html', context)
        # else:
            # return render(request, 'Hr/403.html')
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
def manage_Leave_employee(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_leave_employee':
                if request.user.has_perm('Hr.add_employee_leave'):
                    try:
                        file = request.FILES['documents']
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
                                    'pdf', 'txt', ]
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

                    leave_employee_id = request.POST.get('userIDs')
                    leave_cotegry = request.POST.get('exit_cotegory_id')
                    Discription = request.POST.get('exit_reason')
                    start_day = request.POST.get('date_started')
                    end_day = request.POST.get('date_ended')



                    if leave_employee_id == '' or leave_employee_id == 'null' or leave_employee_id is None or leave_employee_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Employee name' + leave_employee_id + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if leave_cotegry == '' or leave_cotegry == 'null' or leave_cotegry is None or leave_cotegry == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter exit category name' + leave_cotegry + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Discription == '' or Discription == 'null' or Discription is None or Discription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter description ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    get_employe = Employee.objects.get(id=leave_employee_id)

                    if get_employe.Employee_state == "Pending" or get_employe.Employee_state == "Rejected":
                        return JsonResponse(

                            {
                                'isError': True,
                                'Message':  get_employe.get_full_name() + " is Pending or Reject State",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )



                   
                    if start_day == '' or end_day == '' :
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter start date and end day or check your end day maybe same start day or less ' ,
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if end_day < start_day:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'ending day must be older then start day ' ,
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    print(type(start_day))
                    start_days = start_day.split('-')
                    print(start_days, "ayana wadaa")
                    start_days = date(int(start_days[0]), int(start_days[1]), int(start_days[2]))
                    print(type(start_days))
                    if  currentDate >= start_days:
                            
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Start must be equal or greater then current date' ,
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    total = difference_date(start_day, end_day)                      
                    getleaveCatdays = LeaveCatogory.objects.get(id = leave_cotegry)

                    if total > getleaveCatdays.n_days:
                          return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': f'you can only take {getleaveCatdays.n_days} days which assigned for ({getleaveCatdays.name}) ' ,
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                    

                   
                    Discription = RemoveSpecialCharacters(Discription)
                    exit_employe_save = Employee_Leave(
                        employee = get_employe, startday = start_day, endtday = end_day , reason =  Discription ,document = file, leave_ct_id = leave_cotegry ,leavesdays = total )
                    exit_employe_save.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'new leave has been created',
                            'title': 'Successfull !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Dont have permission to add employee exit ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })        
            
            if activity == 'update_leave_employee':
                if request.user.has_perm('Hr.change_employee_leave'):
                    try:
                        file = request.FILES['documents']
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
                                    'pdf', 'txt', ]
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

                    leave_employee_id = request.POST.get('userIDs')
                    leave_cotegry = request.POST.get('exit_cotegory_id')
                    Discription = request.POST.get('exit_reason')
                    start_day = request.POST.get('date_started')
                    end_day = request.POST.get('date_ended')
                    id = request.POST.get('id')

                    if leave_employee_id == '' or leave_employee_id == 'null' or leave_employee_id is None or leave_employee_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Employee name' + leave_employee_id + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if leave_cotegry == '' or leave_cotegry == 'null' or leave_cotegry is None or leave_cotegry == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter exit category name' + leave_cotegry + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Discription == '' or Discription == 'null' or Discription is None or Discription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter description ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    get_employe = Employee.objects.get(id=leave_employee_id)        
                
                    if start_day == '' or end_day == '' :
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter start date and end day or check your end day maybe same start day or less ' ,
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )

                    Discription = RemoveSpecialCharacters(Discription)
                    update_leave =Employee_Leave.objects.get(id = id)
                    update_leave.employee = get_employe
                    update_leave.startday = start_day
                    update_leave.endtday = end_day
                    update_leave.State = 'Pending'
                    update_leave.reason = Discription
                    update_leave.document = file
                    update_leave.leave_ct_id = leave_cotegry
                    update_leave.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f' { update_leave.employee.get_full_name()} leave is apdated',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Dont have permission to add employee exit ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        })        
        
            
            if activity == "get_exit_employee":
                if request.user.has_perm('Hr. view_employee_leave'):
                    single_exit_cotegory = exited_employee.objects.all()
                    message = []
                    for xcotegory in range(0, len(single_exit_cotegory)):
                        message.append({
                            'id': single_exit_cotegory[xcotegory].id,
                            'employee_name': single_exit_cotegory[xcotegory].exit_emp.get_full_name,
                            'category_name': single_exit_cotegory[xcotegory].exit_emp_category.category_name,


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
            if activity == "get_leave_detail":
                if request.user.has_perm('Hr.view_employee_leave'):
                    id = request.POST.get('id')              
                    getexisteempl = Employee_Leave.objects.filter(
                        id=id)
                    message = []
                    for xexited in range(0, len(getexisteempl)):
                        total =   getexisteempl[xexited].endtday - currentDate                      
                        if currentDate == getexisteempl[xexited].endtday:
                            total = 'Completed '
                        if currentDate > getexisteempl[xexited].endtday:
                            total = 'Completed '
                        else:
                            total = get_modified_date(total)
                            
                        message.append({
                            'id': getexisteempl[xexited].id,
                            'empIDss': getexisteempl[xexited].employee.id,
                            'employe_name': getexisteempl[xexited].employee.get_full_name(),
                            'category': getexisteempl[xexited].leave_ct.id,
                            'reason': getexisteempl[xexited].reason,
                            'start': getexisteempl[xexited].startday,
                            'end': getexisteempl[xexited].endtday,                       
                            'approvedWho':"not Approved yet"if getexisteempl[xexited].approvedBy is None else getexisteempl[xexited].approvedBy,                       
                            'update': getexisteempl[xexited].get_modified_date(),                       
                            'Created': getexisteempl[xexited].date_format(),                       
                            'leaveday': total,                       

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Dont have permission to view employee exit ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })  
            if activity == 'approve_reject_exit':
                if request.user.has_perm('Hr.Approve_employee'):
                    # Get all data from the request

                    ID = request.POST.get('ID')
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

                    if ID == '' or ID == 'null' or ID is None or ID == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose State',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if status == 'Confirmed':
                        emplstat = Employee_Leave.objects.get(id=ID)   
                        emplstat.State = status     
                        emplstat.approvedBy = request.user.username                       
                        emplstat.leavesdays =  (emplstat.endtday - emplstat.startday) 
                        emplstat.leavesdays = get_modified_date(emplstat.leavesdays)
                        emplstat.save()
                        return JsonResponse(
                            {
                                'isError': False,
                                'Message': '  updated',
                                'title':  " has been successfully ",
                                'type': 'success',
                            }
                        )

                    if status == 'Returned':
                        print(status + ' ayan wadaa')
                        if Employee_Leave.objects.filter(id=ID).exists():         
                            emplstat = Employee_Leave.objects.get(id=ID)   
                            emplstat.State = status  
                            emplstat.approvedBy = request.user.username
                            emplstat.save()
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
                                    'Message': 'this exited is not exist check your previous exited employee',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if status == 'Rejected':
                        print(status + 'ayan wadaa')
                        if Employee_Leave.objects.filter(id=ID).exists():
                            exitedState = Employee_Leave.objects.get(id=ID)
                            employeeD = exitedState.employee.id
                            exitedState.delete()
                            getemp = Employee.objects.get(id = employeeD)
                            getemp.is_terminated = False
                            getemp.save()
                            return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'this exited is been deleted',
                                    'title':  " has been successfully ",
                                    'type': 'success',
                                }
                            )
                        else:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'this exited is not exist check your previous exited employee',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if activity == "get_employee_name":
                
                    employee_id = request.POST.get('employee_id')

                    all_specialization = Employee.objects.filter(id=employee_id)
                    message = []
                    for xspecilization in range(0, len(all_specialization)):
                        message.append({

                            'id': all_specialization[xspecilization].id,
                            'fullname': all_specialization[xspecilization].first_name,


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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)


def SearchEngine(request):
    try:
        search = request.POST.get('employee')   
        if request.method == 'POST':
            searchQuery = Employee.objects.filter(
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(father_name__icontains=search),
                is_terminated=False,
                Employee_state = "Approved"

                )

            message = []

            for xSearch in range(0, len(searchQuery)):

                message.append({
                    'label': f"{searchQuery[xSearch].emp_number} - {searchQuery[xSearch].first_name} {searchQuery[xSearch].father_name} {searchQuery[xSearch].last_name} ",
                    'userid': searchQuery[xSearch].id,
                },
                )
            return JsonResponse({'Message': message}, status=200)

    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)