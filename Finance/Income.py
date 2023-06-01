from django.shortcuts import render, redirect
from Hr.views import *
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


# Create your views here.
@login_required(login_url='Login')
def main_account(request):
    try:
        # if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Jobtitle = 'All'
            DataNumber = 5
            SearchQuery = ''
            incomes_source = []

            if Checkjobtitle:
                Jobtitle = request.GET['Jobtitle']

            dataFiltering = {}
            if Jobtitle != 'All':
                dataFiltering['job_type_id'] = Jobtitle

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                incomes_source = MainAccount.objects.filter(
                    Q(name__icontains=SearchQuery),
                )
            else:
                incomes_source = MainAccount.objects.all(
               )

            paginator = Paginator(incomes_source, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'Jobtitle': Jobtitle,   
                
            }
            return render(request, 'finances/MainAccount.html',context)

        # else:
        #     return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request, 'finances/MainAccount.html')


@login_required(login_url='Login')
def ManageMainAccount(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'New_account':
                # if request.user.has_perm('Hr.add_employee_exit_category'):    
                    name = request.POST.get('name')
                    account = request.POST.get('account')
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter account name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if account == '' or account == 'null' or account is None or account == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter  account number' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only  ' + name ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    save_account = MainAccount(
                        name=name ,Account = account)
                    save_account.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new account called {name}  has been created',
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
       
       
        # if activity == "get_exit_cotegory":
        #     if request.method == 'POST':
                
        #         single_exit_cotegory = Employee_exit_Category.objects.all()
        #         message = []
        #         for xcotegory in range(0, len(single_exit_cotegory)):
        #             message.append({
        #                 'id': single_exit_cotegory[xcotegory].id,
        #                 'category_name': single_exit_cotegory[xcotegory].category_name,


        #             })
        #         return JsonResponse({'isError': False, 'Message': message}, status=200)

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
def incomeSources(request):
    try:
        # if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Jobtitle = 'All'
            DataNumber = 30
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
                EmployeeList = IncomeSource.objects.filter(
                    Q(name__icontains=SearchQuery) ,
                )
            else:
                EmployeeList = IncomeSource.objects.all(
               )

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'isError': False,
                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                
            }            
            return render(request,'finances/incomeSource.html',context)

        # else:
        #     return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request,'finances/incomeSource.html')



@login_required(login_url='Login')
def ManageIncomeSource(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_income_source':
                # if request.user.has_perm('Hr.add_employee_exit_category'):    
                    name = request.POST.get('name')                   
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Source name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )


                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only  ' + name ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    name = RemoveSpecialCharacters(name)
                    save_account = IncomeSource(
                        name=name )
                    save_account.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new source income called: {name}  is been created',
                            'title': 'successfully created!',
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
            if activity == "update_income_source":
                sourceid = request.POST.get('id')
                name = request.POST.get('name')    
                if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Source name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                name = RemoveSpecialCharacters(name)        
                updateincomesource = IncomeSource.objects.get(id = sourceid)
                updateincomesource.name = name
                updateincomesource.save()

                return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new account called {name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
            if activity == "get_income_source_data":
                sourceid = request.POST.get('id')
                if sourceid == '' or sourceid == None or sourceid == 'undifined':
                     return JsonResponse(
                          {
                                'isError': True,
                                'Message': 'Please enter Source name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            })
                getsourceincome = IncomeSource.objects.get(id = sourceid)

                message= {
                     'id' : getsourceincome.id,
                     'name' : getsourceincome.name
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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)





@login_required(login_url='Login')
def cashtransfer(request):
    try:
        # if request.user.has_perm('Hr.view_employee'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            Checkjobtitle = 'Jobtitle' in request.GET
            Jobtitle = 'All'
            DataNumber = 30
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
                EmployeeList = IncomeSource.objects.filter(
                    Q(name__icontains=SearchQuery) ,
                )
            else:
                EmployeeList = IncomeSource.objects.all(
               )

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'isError': False,
                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                
            }            
            return render(request,'finances/incometransfer.html',context)

        # else:
        #     return render(request, 'Hr/403.html')
    except Exception as error:
        username = request.user.username
        name = request.user.first_name + ' ' + request.user.last_name
        sendException(
            request, username, name, error)
        context = {
            'isError': True,
            'Message': f'On Error Occurs  .{error} Please try again or contact system administrator'
        }
        return render(request,'finances/incomeSource.html')




@login_required(login_url='Login')
def Manage_transfer_cash(request, activity):
    try:
        if request.method == 'POST':
            if activity == 'new_income_source':
                # if request.user.has_perm('Hr.add_employee_exit_category'):    
                    name = request.POST.get('name')                   
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Source name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )


                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only  ' + name ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    name = RemoveSpecialCharacters(name)
                    save_account = IncomeSource(
                        name=name )
                    save_account.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new source income called: {name}  is been created',
                            'title': 'successfully created!',
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
            if activity == "update_income_source":
                sourceid = request.POST.get('id')
                name = request.POST.get('name')    
                if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Source name' ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                name = RemoveSpecialCharacters(name)        
                updateincomesource = IncomeSource.objects.get(id = sourceid)
                updateincomesource.name = name
                updateincomesource.save()

                return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new account called {name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
            if activity == "get_all_main_banks":
                message = []
                id = request.POST.get('ID')
                if id == 'All':
                    getAccountNames = MainAccount.objects.all()                  
                    for xAccountName in range(0, len(getAccountNames)):

                        message.append({
                                'id': getAccountNames[xAccountName].id,                    
                                'name': getAccountNames[xAccountName].name,                      
                            }),
                        
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:                     
                    getAccountNames = MainAccount.objects.filter(~Q(id = id))                 
                    for xAccountName in range(0, len(getAccountNames)):

                        message.append({
                                'id': getAccountNames[xAccountName].id,                    
                                'name': getAccountNames[xAccountName].name,                      
                            }),
                        
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
            if activity == "get_all_income_source":
                message = []
                getincomesource = IncomeSource.objects.all()
                print(getincomesource, 'waa account messha ku jira')

                for xincome_source in range(0, len(getincomesource)):
                 
                    message.append({
                            'id': getincomesource[xincome_source].id,                    
                            'name': getincomesource[xincome_source].name,                      
                        }),                
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


