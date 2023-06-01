from django.db.models.deletion import RestrictedError
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import httpagentparser
from Hr.models import *
from .models import *
from django.contrib.auth import login, authenticate,  logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import JsonResponse
import traceback
import sys
import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


currentTime = datetime.datetime.today()


def Login(request):
    # Checking if the user is logged in
    if request.user.is_authenticated == False:
        # Checking if the send request
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            # create instance from the user
            user = authenticate(email=email, password=password)
            check = Users.objects.filter(
                email=email)
            if len(check) > 0:
                is_active = check_password(password, check[0].password)
                username = check[0].username
                avatar = str(check[0].avatar)
                name = check[0].first_name + ' ' + check[0].last_name
            else:
                is_active = False
            # check if user created
            if user is not None:
                login(request, user)
                action = name + " ayaa system-ka soo galay "
                module = "Users Module"
                path = request.path
                sendTrials(request, username, name,
                           avatar, action, module, path)

                return redirect('dashboard')

            else:
                if is_active:
                    return render(request, 'user/login.html', {'Message': 'Your account is Inactive. Contact to the office'})
                else:
                    return render(request, 'user/login.html', {'Message': 'Email or Password is invalid'})

        return render(request, 'user/login.html')
    else:
        return redirect('dashboard')


def Logout(request):
    username = request.user.username
    name = request.user.get_full_name()
    avatar = str(request.user.avatar)
    module = "Users Module"
    action = name + " Logged out the System"
    path = request.path
    sendTrials(request, username, name, avatar, action, module, path)
    logout(request)
    return redirect('Logout_user')


def LoggedOut(request):
    return render(request, 'user/logout.html')


def sendTrials(request, username, name, avatar, action, module, path, model='', brand=''):
    username = username
    name = name
    avatar = avatar
    ip = request.META.get('REMOTE_ADDR')
    get_client_agent = request.META['HTTP_USER_AGENT']
    try:
        detect_os = httpagentparser.detect(
            get_client_agent)['os']['name']
    except KeyError:
        detect_os = get_client_agent
    try:
        browser = httpagentparser.detect(get_client_agent)[
            'browser']['name']
    except KeyError:
        browser = get_client_agent
    action = action
    module = module
    user_agent = str(ip) + ","
    user_agent += str(detect_os) + ',' if brand == '' else brand + ','
    user_agent += browser if model == '' else model
    audit_trails = AuditTrials(
        Avatar=avatar,
        Name=name,
        Username=username,
        Actions=action,
        path=path,
        Module=module,
        operating_system=detect_os if brand == '' else brand,
        ip_address=ip,
        browser=browser if model == '' else model,
        user_agent=user_agent)

    audit_trails.save()

    return {
        'title': "Audit Trials Saved Successfully!!",
    }


def PreviewDate(date_string, is_datetime, add_time=True):
    if is_datetime:
        new_date = date_string
        if add_time:
            date_string = new_date.strftime("%a") + ', ' + new_date.strftime(
                "%b") + ' ' + str(new_date.day) + ', ' + str(new_date.year) + '  ' + new_date.strftime("%I") + ':' + new_date.strftime("%M") + ':' + new_date.strftime("%S") + ' ' + new_date.strftime("%p")
        else:
            date_string = new_date.strftime("%a") + ', ' + new_date.strftime(
                "%b") + ' ' + str(new_date.day) + ', ' + str(new_date.year)
    else:
        date_string = str(date_string)
        date_string = date_string.split('-')

        new_date = datetime(int(date_string[0]), int(
            date_string[1]), int(date_string[2]))

        date_string = new_date.strftime("%a") + ', ' + new_date.strftime(
            "%b") + ' ' + str(new_date.day) + ', ' + str(new_date.year)

    return date_string


def sendException(request, username, name, error, avatar='', model='', brand=''):
    username = username
    Name = name
    ip = request.META.get('REMOTE_ADDR')
    get_client_agent = request.META['HTTP_USER_AGENT']
    try:
        detect_os = httpagentparser.detect(
            get_client_agent)['os']['name']
    except KeyError:
        detect_os = get_client_agent
    try:
        browser = httpagentparser.detect(get_client_agent)[
            'browser']['name']
    except KeyError:
        browser = get_client_agent
    trace_err = traceback.format_exc()
    Expected_error = str(sys.exc_info()[0])
    field_error = str(sys.exc_info()[1])
    line_number = str(sys.exc_info()[-1].tb_lineno)
    user_agent = str(ip) + ","
    user_agent += str(detect_os) + ',' if brand == '' else brand + ','
    user_agent += browser if model == '' else model
    error_logs = ErrorLogs(
        Avatar=str(request.user.avatar) if avatar == '' else avatar,
        Name=Name,
        Username=username,
        ip_address=ip,
        browser=browser if model == '' else model,
        Expected_error=Expected_error,
        field_error=field_error,
        trace_back=str(trace_err),
        line_number=line_number,
        user_agent=user_agent)

    error_logs.save()

    return {
        'error': str(error),
        'isError': True,
        'title': "An error occurred please contact us"
    }


@login_required(login_url='Login')
def userProfile(request):
    return render(request, 'user/Account.html')



# # Users List
@login_required(login_url='Login')
def UsersList(request):
    if request.user.has_perm('Users.view_users'):
        CheckSearchQuery = 'SearchQuery' in request.GET
        CheckDataNumber = 'DataNumber' in request.GET
        DataNumber = 10
        SearchQuery = ''
        UsersList = []

        if CheckDataNumber:
            DataNumber = int(request.GET['DataNumber'])

        if CheckSearchQuery:
            SearchQuery = request.GET['SearchQuery']
            UsersList = Users.objects.filter(Q(username__icontains=SearchQuery) | Q(email__icontains=SearchQuery) | Q(
                first_name__icontains=SearchQuery) | Q(last_name__icontains=SearchQuery) | Q(phone__icontains=SearchQuery), Q(is_superuser=True) | Q(is_admin=True), is_active=True)
        else:
            UsersList = Users.objects.filter(
                Q(is_superuser=False) | Q(is_admin=True), )

        paginator = Paginator(UsersList, DataNumber)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        Pages = paginator.get_elided_page_range(
            page_obj.number, on_each_side=0, on_ends=1)

        context = {
            'page_obj': page_obj,
            'SearchQuery': SearchQuery,
            'DataNumber': DataNumber,
            'TotalUsers': len(UsersList),
            'Pages': Pages,
            'pageTitle': 'Users List'
        }

        return render(request, 'user/userList.html', context)
    else:
        return render(request, 'Hr/403.html')


@login_required(login_url='Login')
def AuditTrialss(request):
    if request.user.has_perm('Users.view_audittrials'):
        # Checking if these values been sent throught GET Request Method
        CheckSearchQuery = 'SearchQuery' in request.GET
        CheckDataNumber = 'DataNumber' in request.GET
        DataNumber = 5
        SearchQuery = ''
        Audits = ''

        if CheckDataNumber:
            DataNumber = int(request.GET['DataNumber'])

        if CheckSearchQuery:
            SearchQuery = request.GET['SearchQuery']
            Audits = AuditTrials.objects.filter(Q(Username__icontains=SearchQuery) | Q(Name__icontains=SearchQuery) | Q(Module__icontains=SearchQuery) | Q(
                Actions__icontains=SearchQuery) | Q(date_of_action__icontains=SearchQuery) | Q(user_agent__icontains=SearchQuery)).order_by('-date_of_action')
        else:
            Audits = AuditTrials.objects.all().order_by('-date_of_action')

        paginator = Paginator(Audits, DataNumber)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        Pages = list(paginator.get_elided_page_range(
            page_obj.number, on_each_side=0, on_ends=1))

        context = {
            'page_obj': page_obj,
            'SearchQuery': SearchQuery,
            'DataNumber': DataNumber,
            'TotalUsers': len(Audits),
            'Pages': Pages,
            'pageTitle': 'Audit Trials'
        }
        return render(request, 'Logs/audit_trial.html', context)
    else:
        return render(request, 'Hr/403.html')


@login_required(login_url='Login')
def ErrorLogss(request):
    if request.user.has_perm('Users.view_errorlogs'):
        # Checking if these values been sent throught GET Request Method
        CheckSearchQuery = 'SearchQuery' in request.GET
        CheckDataNumber = 'DataNumber' in request.GET
        DataNumber = 5
        SearchQuery = ''
        Errors = ''

        if CheckDataNumber:
            DataNumber = int(request.GET['DataNumber'])

        if CheckSearchQuery:
            SearchQuery = request.GET['SearchQuery']
            Errors = ErrorLogs.objects.filter(Q(Username__icontains=SearchQuery) | Q(Name__icontains=SearchQuery) | Q(Expected_error__icontains=SearchQuery) | Q(
                field_error__icontains=SearchQuery) | Q(line_number__icontains=SearchQuery) | Q(date_recorded__icontains=SearchQuery) | Q(user_agent__icontains=SearchQuery)).order_by('-date_recorded')
        else:
            Errors = ErrorLogs.objects.all().order_by('-date_recorded')

        paginator = Paginator(Errors, DataNumber)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        Pages = list(paginator.get_elided_page_range(
            page_obj.number, on_each_side=1, on_ends=1))

        context = {
            'page_obj': page_obj,
            'SearchQuery': SearchQuery,
            'DataNumber': DataNumber,
            'pageTitle': 'Error Logs',
        }
        return render(request, 'Logs/errors_logs.html', context)
    else:
        return render(request, 'Hr/403.html')


@login_required(login_url='Login')
def ManageErrorLogs(request, action):
    if action == "AuditTrial":
        if request.method == 'POST':
            if request.user.has_perm('Users.view_audittrials'):
                try:
                    id = request.POST.get('id')
                    trial = AuditTrials.objects.get(id=id)

                    message = {
                        'ID': trial.id,
                        'Trial': trial.Actions,
                        'Path': trial.path,
                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

    if action == 'ErrorLogs':
        if request.method == 'POST':
            if request.user.has_perm('Users.view_errorlogs'):
                try:
                    id = request.POST.get('id')
                    logs = ErrorLogs.objects.get(id=id)

                    message = {
                        'ID': logs.id,
                        'TraceBack': logs.trace_back
                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)


@login_required(login_url='Login')
def EmployeeList(request):
    try:
        if request.user.has_perm('Users.view_users'):
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
                EmployeeList = JobDetails.objects.filter(

                    Q(employee__job_type__name__icontains=SearchQuery) |
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__father_name__icontains=SearchQuery) |
                    Q(employee__last_name__icontains=SearchQuery) |
                    Q(employee__emp_number__icontains=SearchQuery) |
                    Q(employee__gender__icontains=SearchQuery),
                    **dataFiltering,
                    employee__Employee_state="Approved",
                    employee__is_terminated=False,
                    # job_state = True,
                    is_active=True,
                    job_state="Approved",



                )
            else:
                EmployeeList = JobDetails.objects.filter(
                    **dataFiltering,
                    employee__Employee_state="Approved",
                    employee__is_terminated=False,
                    is_active=True,
                    job_state="Approved",
                )

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,
                'pageTitle': 'Employee List',
                'all_Department': Departments.objects.all(),

            }
            return render(request, 'user/UserCreation.html', context)

        else:
            return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs   .{error} Please try again or contact system administrator'
        }
        return render(request, 'user/UserCreation.html', context)


@login_required(login_url='Login')
def Manage_user(request, action):
    try:
        if action == 'NewUser':
            if request.method == 'POST':
                if request.user.has_perm('Users.add_users'):
                    employee_number = request.POST.get('employee_id')
                    email = request.POST.get('email')

                    if email == '' or email is None:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Enter Email',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if employee_number == '' or employee_number is None:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Specify Employee Number',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Users.objects.filter(email=email).exists():
                        email_belong_to = Users.objects.get(email=email)
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': f'{email} is belong to someone',
                                'title': ' Email Checking!',
                                'type': 'warning',
                            }
                        )

                    employee_number = Employee.objects.get(
                        id=employee_number)

                    response = Users.create_user(
                        f"{employee_number.first_name} {employee_number.father_name}", f"{employee_number.last_name} ", email, employee_number.phone,  employee_number.gender,  employee_number.photo, False, True, False, request, employee_number.id,)

                    if response['isError'] == False:
                        username = request.user.username
                        names = request.user.first_name + ' ' + request.user.last_name
                        avatar = str(request.user.avatar)
                        module = "Users Module / users Table"
                        action = f"{names} wuxuu user u abuuray shaqaalaha lagu magacaabo {employee_number.first_name} {employee_number.father_name} {employee_number.last_name}"
                        path = request.path
                        sendTrials(request, username, names,
                                   avatar, action, module, path)
                        message = {
                            'isError': False,
                            'Message': f"New user has been created for {employee_number.get_full_name()}"
                        }
                        return JsonResponse(message, status=200)
                    else:
                        return JsonResponse(response, status=200)
                else:
                    message = {
                        'isError': True,
                        'Message': '403-Unauthorized access.you do not have permission to access this page.'
                    }
                    return JsonResponse(message, status=200)
        if action == "get_employee_data":
            id = request.POST.get('id')
            empl = Employee.objects.get(id=id)
            message = []
            message = {
                "id": empl.id,
                "email": empl.email,
            }
            return JsonResponse({'isError': False, 'Message': message}, status=200)
        if action == "activate_user":
            userIDs = request.POST.get('userIDs')
            type = request.POST.get('type')
            getuser = Users.objects.get(id=userIDs)

            if type == 'activate':
                getuser.is_active = True
                getuser.save()
                return JsonResponse(
                    {
                        'isError': False,
                        'title': f'Are you sure to {type} ',
                        'Message':f'{getuser.first_name } will be Active ',
                        'type': 'warning',
                    }
                )

            else:
                getuser.is_active = False
                getuser.save()
                return JsonResponse(
                    {
                        'isError': False,
                        'title': f'Are you sure to {type} ',
                        'Message':f'{getuser.first_name } will be InActive',
                        'type': 'warning',
                    }
                )           
         
        if action == "ChangeUserPassword":
             if request.method == 'POST':
                CurrentPassword = request.POST.get('CurrentPassword')
                newPassword = request.POST.get('newPassword')
                CormfirmPassword = request.POST.get('CormfirmPassword')
                userID = request.user.id  
                if CurrentPassword == '' or CurrentPassword == 'null' or CurrentPassword is None or CurrentPassword == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Current Password',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                if newPassword == '' or newPassword == 'null' or newPassword is None or newPassword == 'undefined' :
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter New Password',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                if CormfirmPassword == '' or CormfirmPassword == 'null' or CormfirmPassword is None or CormfirmPassword == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Confirmaton Password',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                currentuser = Users.objects.get(id = userID)                
                if check_password(CurrentPassword, currentuser.password): 
                    if newPassword == CormfirmPassword:
                        currentuser.set_password(newPassword)
                        currentuser.save()                           
                        return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'Password  changed successfully',
                                    'title': 'Successfully!',
                                    'type': 'success',
                                }
                                )
                    else:
                        return JsonResponse(
                            {
                            'isError': True,
                            'Message':'new password and confirmation password not matching',
                            'title': 'Validation Error!',
                            'type': 'warning',

                                }
                            )
                    
                else:
                     return JsonResponse(
                            {
                            'isError': True,
                            'Message':'Incorrect Current Password',
                            'title': 'Validation Error!',
                            'type': 'warning',

                                }
                            )
        if action == "change_profile_picture":
            userids = request.user.id  
            currentuser = Users.objects.get(id = userids)

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
            currentuser.avatar = file
            currentuser.save()
            return JsonResponse(
                {
                    'isError': False,
                    'Message': 'profile picture changed successfully',
                    'title': 'Successfully!',
                    'type': 'success',
                }
                )
        if action == "Edit_user_data":
            usernames = request.POST.get('user_username')
            first_name = request.POST.get('user_firstname')
            midle_name = request.POST.get('user_lastname')
            gender = request.POST.get('user_gender')
            emails = request.POST.get('user_email')

            userid = request.user.id
            currentuser = Users.objects.get(id  = userid)


            currentuser.username  = usernames 
            currentuser.first_name = first_name 
            currentuser.last_name = midle_name
            currentuser.gender = gender 
            currentuser.email = emails
            currentuser.save() 
            return JsonResponse(
                {
                    'isError': False,
                    'Message': 'User info succesfully updated',
                    'title': 'Successfully!',
                    'type': 'success',
                }
                )

           
  
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        message = {
            'isError': True,
            'Message': f'On Error Occurs .{error} Please try again or contact system administrator'
        }
        return JsonResponse({'isError': True, 'Message': message}, status=200)


# User Roles Report
@login_required(login_url='Login')
def ViewUserRolesReportPage(request):
    if request.user.has_perm('auth.view_permission'):
        context = {
            'pageTitle': 'User Roles Report'
        }
        return render(request, 'Roles/user_role_report.html', context)
    else:
        return render(request, 'Hr/403.html')

# Serach Roles


@login_required(login_url='Login')
def SearchRole(request):
    if request.user.has_perm('auth.add_permission') and request.user.has_perm('auth.view_permission') or request.user.has_perm('Users.manage_role_groups'):
        CheckSearch = 'Search' in request.GET

        context = {
            'Message': '',
            'Search': '',
            'pageTitle': 'Search Role'
        }

        if CheckSearch:
            Search = request.GET['Search']
            context['Search'] = Search

            # Check if the role exists
            check_permisison = Permission.objects.filter(codename=Search)

            if len(check_permisison) == 0:
                context['Message'] = 'This role does not exist'
            else:
                check_permisison = check_permisison[0]
                context["App"] = check_permisison.content_type.app_label
                context["Model"] = check_permisison.content_type.model
                context['Message'] = 'Yes'

        return render(request, 'Roles/search_role.html', context)
    else:
        return render(request, 'Base/401.html')


# Roles Report
@login_required(login_url='Login')
def ViewRolesReportPage(request):
    if request.user.has_perm('Users.role_report'):
        context = {
            'pageTitle': 'Roles Report'
        }
        return render(request, 'Roles/role_report.html', context)
    else:
        return render(request, 'Base/401.html')

# Assign Role


@login_required(login_url='Login')
def ViewRolesPage(request):
    if request.user.has_perm('auth.view_permission') and request.user.has_perm('auth.add_permission'):
        context = {
            'pageTitle': 'Assign Role To User'
        }
        return render(request, 'Roles/assign_role.html', context)
    else:
        return render(request, 'Hr/403.html')


# Edit Group Roles
@login_required(login_url='Login')
def ViewEditGroupPage(request, group_id):
    if request.user.has_perm('auth.view_group'):
        context = {
            'pageTitle': 'Edit Group Roles',
            'GroupID': group_id
        }
        return render(request, 'Roles/edit_group.html', context)
    else:
        return render(request, 'Base/401.html')

# List of groups


@login_required(login_url='Login')
def ViewGroupRolesPage(request):
    if request.user.has_perm('Users.assign_user_to_group'):
        context = {
            'pageTitle': 'Assign User To A Group Role'
        }
        return render(request, 'Roles/assign_group.html', context)
    else:
        return render(request, 'Base/401.html')


@login_required(login_url='Login')
def ViewManageGroupPage(request):
    if request.user.has_perm('auth.view_group'):
        context = {
            'pageTitle': 'Create Groups'
        }
        return render(request, 'Roles/manage_group.html', context)
    else:
        return render(request, 'Hr/403.html')


@login_required(login_url='Login')
def ManagePermission(request, id):

    allowed_users = ['ADM', 'EMP']
    if id == '0':
        if request.method == 'POST':
            if request.user.has_perm('auth.add_permission'):
                Type = request.POST.get('type')
                User = request.POST.get('user')
                PermID = int(request.POST.get('permID'))

                if User[:3] in allowed_users:
                    try:
                        if User[:3] in allowed_users:
                            User = Users.objects.get(username=User)
                        else:
                            User = Users.objects.get(id=int(User))

                        # Get Permisison
                        P = Permission.objects.get(id=PermID)

                        if Type == 'Add':
                            check_if_assigned = Users.objects.filter(
                                user_permissions=P).distinct()

                            if len(check_if_assigned) > 0:
                                user = check_if_assigned[0]

                                if P.codename == 'saxiixa_khasnajiga':
                                    return JsonResponse({'isError': True, 'Message': f'Saxiixa khasnajiga waxaa haysto {user.get_full_name()}'}, status=200)
                                if P.codename == 'waaxda_laanta_saadka':
                                    return JsonResponse({'isError': True, 'Message': f'Saxiixa laanta saadka waxaa haysto {user.get_full_name()}'}, status=200)
                                if P.codename == 'software_signature_role':
                                    return JsonResponse({'isError': True, 'Message': f'Saxiixa waaxda softwareka waxaa haysto {user.get_full_name()}'}, status=200)
                                if P.codename == 'director_signature_role':
                                    return JsonResponse({'isError': True, 'Message': f'Saxiixa agaasinka tiknaloojiyadda waxaa haysto {user.get_full_name()}'}, status=200)
                            User.user_permissions.add(P)
                        else:
                            User.user_permissions.remove(P)

                        username = request.user.username
                        names = request.user.first_name + ' ' + request.user.last_name
                        avatar = str(request.user.avatar)
                        module = "Users-Permission Module"
                        if Type == 'Add':
                            action = 'Granted Permission to' + "_" + \
                                P.codename + " With username of " + User.username
                        else:
                            action = 'Permission Denied to' + "_" + \
                                P.codename + " With username of " + User.username
                        path = request.path
                        sendTrials(request, username, names,
                                   avatar, action, module, path)

                        isError = False
                        message = 'Permission Granted' if Type == 'Add' else 'Permission Denied'
                    except Exception as error:
                        username = request.user.username
                        name = request.user.first_name + ' ' + request.user.last_name
                        sendException(
                            request, username, name, error)
                        message = {
                            'isError': True,
                            'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                        }
                        return JsonResponse(message, status=200)
                else:
                    isError = True
                    message = 'Invalid user or this user specified not allowed for taking permissions'
                return JsonResponse({'isError': isError, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)
    else:
        if request.method == 'GET':
            if request.user.has_perm('auth.view_permission'):
                if id[:3] in allowed_users:
                    if id[:3] in allowed_users:
                        User = Users.objects.filter(username=id)
                    else:
                        User = Users.objects.filter(id=int(id))

                    perms = Permission.objects.all().order_by('content_type')

                    if len(User) > 0:
                        if len(perms) < 0:
                            return JsonResponse({'isError': True, 'Message': 'No Permissions Available'}, status=200)
                        else:
                            id = 0
                            message = []
                            for xPerm in range(0, len(perms)):
                                # Checking if the user has prmisison
                                txt = perms[xPerm].content_type.app_label + \
                                    '.' + perms[xPerm].codename
                                isPermitted = User[0].has_perm(txt)

                                if id != perms[xPerm].content_type.id:

                                    id = perms[xPerm].content_type.id

                                    message.append({
                                        'App': perms[xPerm].content_type.app_label,
                                        'Model': perms[xPerm].content_type.model,
                                        'Actions': [
                                            {
                                                'Action': perms[xPerm].codename,
                                                'ID': perms[xPerm].id,
                                                'isPermitted': isPermitted,
                                                'isSuperuser': User[0].is_superuser
                                            }
                                        ]

                                    })
                                else:
                                    message[len(message) - 1]['Actions'].append({
                                        'Action': perms[xPerm].codename,
                                        'ID': perms[xPerm].id,
                                        'isPermitted': isPermitted,
                                        'isSuperuser': User[0].is_superuser
                                    })

                            return JsonResponse({'isError': False, 'Message': message}, status=200)
                    else:
                        return JsonResponse({'isError': True, 'Message': 'User does not exist'}, status=200)
                else:
                    return JsonResponse({'isError': True, 'Message': 'Invalid user or this user specified not allowed for taking permissions'}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)


@login_required(login_url='Login')
def ManageGroupPermission(request, id, _id):
    allowed_users = ['ADM', 'EMP']
    if id == '0':
        if request.method == 'POST':
            if request.user.has_perm('Users.assign_user_to_group'):
                Type = request.POST.get('type')
                User = request.POST.get('user')
                PermID = int(request.POST.get('permID'))
                if User[:2] in allowed_users:
                    try:
                        if User[:3] in allowed_users:
                            User =Users.objects.get(username=User)
                        else:
                            User = Users.objects.get(id=int(User))
                        # Get Group
                        P = Group.objects.get(id=PermID)

                        if Type == 'Add':
                            User.groups.add(P)
                        else:
                            User.groups.remove(P)
                        username = request.user.username
                        names = request.user.first_name + ' ' + request.user.last_name
                        avatar = str(request.user.avatar)
                        module = "Users-Permission Module"
                        if Type == 'Add':
                            action = "User with username of:" + '_' + \
                                User.username + " added group of " + P.name
                        else:
                            action = "User with username of:" + '_' + \
                                User.username + " removed group of " + P.name
                        path = request.path
                        sendTrials(request, username, names,
                                   avatar, action, module, path)

                        isError = False
                        message = 'User has been added to the group ' if Type == 'Add' else 'User has been removed from the group '
                    except Exception as error:
                        username = request.user.username
                        name = request.user.first_name + ' ' + request.user.last_name
                        sendException(
                            request, username, name, error)
                        message = {
                            'isError': True,
                            'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                        }
                        return JsonResponse(message, status=200)
                else:
                    isError = True
                    message = 'Invalid user or this user specified not allowed for taking permissions'
                return JsonResponse({'isError': isError, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)
    else:
        if request.method == 'GET':
            if request.user.has_perm('auth.view_permission') or request.user.has_perm('Users.assign_user_to_group'):
                if id[:3] in allowed_users:
                    if id[:3] in allowed_users:
                        User = Users.objects.filter(username=id)
                    else:
                        User = Users.objects.filter(id=int(id))

                    groups = Group.objects.all()

                    if len(User) > 0:
                        if len(groups) < 0:
                            return JsonResponse({'isError': True, 'Message': 'No Groups Available'}, status=200)
                        else:
                            id = 0
                            message = []
                            for xGroup in range(0, len(groups)):
                                message.append({
                                    'ID': groups[xGroup].id,
                                    'Count': groups[xGroup].permissions.all().count(),
                                    'Name': groups[xGroup].name,
                                    'IsJoined': True if len(User[0].groups.filter(name=groups[xGroup].name)) > 0 else False,
                                    'IsSuper': True if User[0].is_superuser > 0 else False,
                                })
                            return JsonResponse({'isError': False, 'Message': message}, status=200)
                    else:
                        return JsonResponse({'isError': True, 'Message': 'User does not exist'}, status=200)
                else:
                    return JsonResponse({'isError': True, 'Message': 'Invalid user or this user specified not allowed for taking permissions'}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'POST':
            if request.user.has_perm('auth.view_group') or request.user.has_perm('Users.assign_user_to_group'):
                GroupID = int(id)

                try:
                    # Get Group
                    group = Group.objects.get(id=GroupID)
                    perms = group.permissions.filter(group=group)
                    message = []
                    isError = False
                    for xPerm in range(0, len(perms)):
                        message.append({
                            'Name': perms[xPerm].name,
                            'Codename': perms[xPerm].codename,
                            'ID': perms[xPerm].id,
                            'GroupID': group.id,
                            'App': perms[xPerm].content_type.app_label,
                            'Model': perms[xPerm].content_type.model,
                        })

                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
                return JsonResponse({'isError': isError, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'DELETE':
            if request.user.has_perm('auth.delete_permission') or request.user.has_perm('Users.remove_role_from_group'):
                GroupID = int(id)
                PermID = int(_id)

                try:
                    # Get Group
                    group = Group.objects.get(id=GroupID)
                    permission = Permission.objects.get(id=PermID)
                    # User = models.Users.objects.get(id=GroupID)
                    # Remove From The Group
                    perms = group.permissions.remove(permission)
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Users-Permission Module"
                    action = "User with username of:" + '_' + username + \
                        "removed " + permission.codename + " from the group " + group.name
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)
                    message = 'Permission removed from the group'
                    isError = False

                    return JsonResponse({'isError': isError, 'Message': message}, status=200)

                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete some instances of model because they are referenced through restricted foreign keys'}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)


@login_required(login_url='Login')
def PermissonReport(request):
    if request.method == 'POST':
        if request.user.has_perm('Users.role_report'):
            Type = request.POST.get('type')
            message = ''
            Apps = []
            Modal = []
            Codes = []

            if Type == 'GetGroups':
                list = []
                groups = Group.objects.all()
                for xgroup in range(0, len(groups)):
                    list.append({
                        'GroupName': groups[xgroup].name,
                        'GroupID': groups[xgroup].id,
                    })
                message = {
                    'isError': False, 'Message': list
                }

            elif Type == 'GetApps':
                list = []
                contentType = ContentType.objects.all()
                for xApp in range(0, len(contentType)):
                    is_added = contentType[xApp].app_label in Apps
                    if is_added == False:
                        Apps.append(contentType[xApp].app_label)
                        list.append({
                            'AppName': contentType[xApp].app_label,
                        })
                message = {
                    'isError': False, 'Message': list
                }

            elif Type == 'GetModals':
                App = request.POST.get('app')
                list = []
                contentType = ContentType.objects.filter(app_label=App)
                for xModal in range(0, len(contentType)):
                    is_added = contentType[xModal].model in Modal
                    if is_added == False:
                        Modal.append(contentType[xModal].model)
                        list.append({
                            'ModalName': contentType[xModal].model,
                        })
                message = {
                    'isError': False, 'Message': list
                }

            elif Type == 'GetCodes':
                try:
                    App = request.POST.get('app')
                    Modal = request.POST.get('modal')
                    list = []
                    contentType = ContentType.objects.get(
                        app_label=App, model=Modal)
                    perms = Permission.objects.filter(
                        content_type=contentType.id)
                    for xCode in range(0, len(perms)):
                        list.append({
                            'CodeName': perms[xCode].codename,
                            'ContentID': perms[xCode].content_type.id,
                            'PermID': perms[xCode].id,
                        })
                    message = {
                        'isError': False, 'Message': list
                    }
                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} {error}. Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
            elif Type == 'GetReport':
                report = request.POST.get('report')
                app = request.POST.get('app')
                modal = request.POST.get('modal')
                code = request.POST.get('code')
                group = request.POST.get('group')

                try:
                    list = []

                    if report == 'Role':
                        perm = Permission.objects.get(codename=code)
                        users = Users.objects.filter(
                            Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()

                        for xUser in range(0, len(users)):
                            avatar = users[xUser].avatar
                            list.append({
                                'Username': users[xUser].username,
                                'Name': users[xUser].first_name + ' ' + users[xUser].last_name,
                                'Email': users[xUser].email,
                                'Avatar': str(avatar)
                            })
                        message = {
                            'isError': False, 'Message': list
                        }

                    elif report == 'Group':
                        perm = Group.objects.get(name=group)
                        users = perm.user_set.all()

                        for xUser in range(0, len(users)):
                            avatar = users[xUser].avatar
                            list.append({
                                'Username': users[xUser].username,
                                'Name': users[xUser].first_name + ' ' + users[xUser].last_name,
                                'Email': users[xUser].email,
                                'Avatar': str(avatar)
                            })
                        message = {
                            'isError': False, 'Message': list
                        }

                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)

            elif Type == 'GetUserReport':
                try:
                    report = request.POST.get('report')
                    user = request.POST.get('user')
                    userInstance = Users.objects.get(id=int(user))

                    list = []
                    if report == 'Role':
                        user_perms = Permission.objects.filter(
                            Q(user=userInstance) | Q(group__user=userInstance))

                        for xPerm in range(0, len(user_perms)):
                            list.append({
                                'App': user_perms[xPerm].content_type.app_label,
                                'Model': user_perms[xPerm].content_type.model,
                                'Codename': user_perms[xPerm].codename
                            })

                        message = {
                            'isError': False,
                            'Message': list
                        }

                    elif report == 'Group':
                        groups = Group.objects.filter(user=userInstance)

                        for xGroup in range(0, len(groups)):
                            list.append({
                                'GroupID': groups[xGroup].id,
                                'GroupName': groups[xGroup].name,
                                'Permissions': groups[xGroup].permissions.all().count(),
                            })

                        message = {
                            'isError': False,
                            'Message': list
                        }

                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)

            return JsonResponse(message, status=200)

        else:
            message = {
                'isError': True,
                'Message': '401-Unauthorized access.you do not have permission to access this page.'
            }
            return JsonResponse(message, status=200)


@login_required(login_url='Login')
def ManageGroup(request, id):
    if id == '0':
        if request.method == 'POST':
            if request.user.has_perm('auth.add_group'):
                Name = request.POST.get('name')

                if Group.objects.filter(name=Name).exists():
                    return JsonResponse({'isError': True, 'Message': 'This Group already exists'})
                else:
                    g = Group(name=Name)
                    g.save()
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Users-Permission Module"
                    action = "Added new Group with Name of:" + '_' + Name
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)

                    return JsonResponse({'isError': False, 'Message': 'New group has been created'})
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'GET':
            if request.user.has_perm('auth.view_group'):
                groups = Group.objects.all()
                if len(groups) < 0:
                    return JsonResponse({'isError': True, 'Message': 'No Groups Available'}, status=200)
                else:
                    id = 0
                    message = []
                    for xGroup in range(0, len(groups)):
                        message.append({
                            'ID': groups[xGroup].id,
                            'Count': groups[xGroup].permissions.all().count(),
                            'Name': groups[xGroup].name,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)
    else:
        if request.method == 'GET':
            if request.user.has_perm('auth.view_group'):
                try:
                    group = Group.objects.get(id=id)

                    unauthorized_perms = [
                        'Approve_employee','Approve_appointment','Approve_visit'
                    ]
                    perms = Permission.objects.filter(
                        ~Q(codename__in=unauthorized_perms),
                    ).order_by('content_type')
                    id = 0
                    message = []
                    for xPerm in range(0, len(perms)):
                        isGiven = True if len(group.permissions.filter(
                            id=perms[xPerm].id)) > 0 else False
                        if id != perms[xPerm].content_type.id:
                            id = perms[xPerm].content_type.id

                            message.append({
                                'App': perms[xPerm].content_type.app_label,
                                'Model': perms[xPerm].content_type.model,
                                'Actions': [
                                    {
                                        'Action': perms[xPerm].codename,
                                        'ID': perms[xPerm].id,
                                        'isGiven': isGiven
                                    }
                                ]

                            })
                        else:
                            message[len(message) - 1]['Actions'].append({
                                'Action': perms[xPerm].codename,
                                'ID': perms[xPerm].id,
                                'isGiven': isGiven
                            })

                    isError = False

                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
                return JsonResponse({'isError': isError, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'POST':
            if request.user.has_perm('Users.manage_role_groups'):
                GroupID = int(id)
                PermID = int(request.POST.get('permID'))
                Type = request.POST.get('type')
                try:
                    # Get Group
                    group = Group.objects.get(id=GroupID)
                    # User = models.Users.objects.get(id=GroupID)
                    permission = Permission.objects.get(id=PermID)
                    # Add To The Group
                    if Type == 'Add':
                        perms = group.permissions.add(permission)
                    else:
                        perms = group.permissions.remove(permission)
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Users-Permission Module"
                    if Type == 'Remove':
                        action = permission.codename + " removed from the group of " + group.name
                    else:
                        action = permission.codename + " Added to the group of " + group.name
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)

                    message = 'Permission removed from the group' if Type == 'Remove' else 'Permission added to the group'
                    isError = False

                except Exception as error:
                    username = request.user.username
                    name = request.user.first_name + ' ' + request.user.last_name
                    sendException(
                        request, username, name, error)
                    message = {
                        'isError': True,
                        'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                    }
                    return JsonResponse(message, status=200)
                return JsonResponse({'isError': isError, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'DELETE':
            if request.user.has_perm('auth.delete_group'):
                try:
                    GroupID = int(id)
                    group = Group.objects.get(id=GroupID)
                    group.delete()
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Users-Permission Module"
                    action = "Deleted Group with Name of:" + '_' + group.name
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)

                    return JsonResponse({'isError': False, 'Message': "Group has been deleted successfully"}, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete some instances of model because they are referenced through restricted foreign keys'}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)

        if request.method == 'PATCH':
            if request.user.has_perm('auth.view_group'):
                GroupID = int(id)
                group = Group.objects.get(id=GroupID)
                message = {
                    'id': group.id,
                    'Name': group.name,
                }
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            else:
                message = {
                    'isError': True,
                    'Message': '401-Unauthorized access.you do not have permission to access this page.'
                }
                return JsonResponse(message, status=200)


@login_required(login_url='Login')
def RenameGroup(request):
    if request.method == 'POST':
        if request.user.has_perm('auth.change_group'):
            Name = request.POST.get('name')
            ID = request.POST.get('ID')

            try:
                G = Group.objects.get(id=ID)
                if Group.objects.filter(name=Name).exists() and Name != G.name:
                    return JsonResponse({'isError': True, 'Message': 'This Group already exists'})
                else:
                    G.name = Name
                    G.save()
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Users-Permission Module"
                    action = "Updated Group with Name of:" + '_' + Name
                    path = request.path
                    sendTrials(request, username, names,
                               avatar, action, module, path)

                    return JsonResponse({'isError': False, 'Message': 'Group has been renamed'})
            except Exception as error:
                username = request.user.username
                name = request.user.first_name + ' ' + request.user.last_name
                sendException(
                    request, username, name, error)
                message = {
                    'isError': True,
                    'Message': f'On Error Occurs  {error} . Please try again or contact system administrator'
                }
                return JsonResponse(message, status=200)
        else:

            message = {
                'isError': True,
                'Message': '401-Unauthorized access.you do not have permission to access this page.'
            }
            return JsonResponse(message, status=200)




# Search Query
@login_required(login_url='Login')
def SearchEngineUser(request, search, type):  
 
    if ',' in type:
        type = type.split(',')
    else:
        type = [type]

    # Searching the users from users table
    # Goes like this:

    if 'FromEmployee' not in type:
        CheckAdmin = False if 'ADM' not in type else True
        CheckAgent = False if 'EMP' not in type else True
        # CheckEmployee = False if type != 'EMM' else True # If Employee Existed Or Diactivated! The Student's Results Of Marks And Attendance Should Be Seen

        searchFields = {}

        if CheckAdmin:
            searchFields['is_admin'] = True
            searchFields['is_superuser'] = True

        if CheckAgent:
            searchFields['is_staff'] = True

        # search_filter = Q(**searchFields, _connector=Q.OR)

        if request.method == 'GET':
            searchQuery = Users.objects.filter(Q(**searchFields, _connector=Q.OR), Q(username__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search) | Q(
                first_name__icontains=search) | Q(last_name__icontains=search), is_active=True ,is_superuser = False)

            message = []
            userType = ''
            for xSearch in range(0, len(searchQuery)):
                if searchQuery[xSearch].is_superuser:
                    userType = 'Superuser'
                elif searchQuery[xSearch].is_admin:
                    userType = 'Admin'
                elif searchQuery[xSearch].is_staff:
                    userType = 'Staff'

                if searchQuery[xSearch].is_active == True:
                    message.append({
                        'label': f"{searchQuery[xSearch].username} - {searchQuery[xSearch].first_name} {searchQuery[xSearch].last_name} ({searchQuery[xSearch].email})",
                        'value': f"{searchQuery[xSearch].username} - {searchQuery[xSearch].first_name} {searchQuery[xSearch].last_name}",
                        'username': searchQuery[xSearch].username,
                        'userid': searchQuery[xSearch].id,
                    },
                    )
            return JsonResponse({'Message': message}, status=200)

    # Searching the users from employee table
    # Goes like this:

    if request.method == 'GET':
        searchQuery = Employee.objects.filter(
            Q(emp_full_name__istartswith=search) | Q(employee_id__istartswith=search) | Q(employee_id__icontains=search), is_active=True, is_emp_exit=False, is_emp_dead=False)

        message = []
        userType = ''
        for xSearch in range(0, len(searchQuery)):
            message.append(
                {
                    'label': f"{searchQuery[xSearch].emp_number} - {searchQuery[xSearch].get_absolute_url}",
                    'value': f"{searchQuery[xSearch].emp_number} - {searchQuery[xSearch].get_absolute_url}",
                    'username': searchQuery[xSearch].emp_number,
                    'userid': searchQuery[xSearch].id,

                }
            )
        return JsonResponse({'Message': message}, status=200)

