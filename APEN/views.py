from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from Hr.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Inventory.models import Medicine, Medicine_categories
from LRPD.models import *
from Users.models import Users
from django.contrib.auth.decorators import permission_required
from Users.models import sendException
from Users.views import sendTrials

# Create your views here.
currentDate = date.today()

# ------------------Patients---------------------------

@login_required(login_url='Login')          
def category_operations_list(request):
    try:
        if request.user.has_perm('APEN.view_operationcategory'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            operation_category_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                operation_category_list =OperationCategory.objects.filter(
                    Q(CategoryName__icontains = SearchQuery) 
                
                    
                )
            else:
                operation_category_list =OperationCategory.objects.all()

            paginator = Paginator(operation_category_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Oprations category List'


            }
            return render (request, 'Operations/operationCategory.html',context)
        else:
            return render(request, 'Hr/404.html')
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
def manage_category_operations(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_category':
                if request.user.has_perm('APEN.add_operationcategory'):
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

                    new_category = OperationCategory(CategoryName = CategoryName, Description= Description)
                    new_category.save()
                
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new Category has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add an prescription',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_category':
                if request.user.has_perm('APEN.change_operations'):
                # Get all data from the request
                    categories_id = request.POST.get('CategoryID')
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

                    
                    update_category= OperationCategory.objects.get(id=categories_id)
                    update_category.CategoryName = CategoryName
                    update_category.Description = Description
                    
                    update_category.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'an Operation Category has been updated',
                                'title': 'masha allah !' + CategoryName + " been updated" ,
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add an prescription',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            
            if action == "get-operation-categories":
                if request.user.has_perm('APEN.change_operations'):
                    id = request.POST.get('category_id')
                
                    category_id = OperationCategory.objects.get(id = id)
                    
            

                    message = {
                        'id': category_id.id,
                        'CategoryName': category_id.CategoryName,
                        'Description': category_id.Description,
                        
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
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
def operations_list(request):
    try:
        if request.user.has_perm('APEN.view_operations'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            operation_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                operation_list =Operations.objects.filter(
                    Q(OperationName__icontains = SearchQuery) |
                    Q(CategoryName__icontains = SearchQuery)      
                )
            else:
                operation_list =Operations.objects.all()

            paginator = Paginator(operation_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Categories = OperationCategory.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Oprations List',
                'categories': Categories,


            }
            return render (request, 'Operations/operations.html',context)

        else:
            return render(request, 'Hr/404.html')
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
def manage_operations(request, action):
    try:
        if request.method == 'POST': 
            if action == 'new_operations':
                if request.user.has_perm('APEN.add_operations'):
                    # Get all data from the request
                    operations = request.POST.get('OperationName')
                    Category = request.POST.get('CategoryName')
                    Description = request.POST.get('Description')
                    # Validaet dat
                    if operations == '' or operations == 'null' or operations is None or operations == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Operation ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Category == '' or Category == 'null' or Category is None or Category == 'undefined':
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
                    category_id = OperationCategory.objects.get(id=Category)
                    new_operation = Operations(OperationName= operations, CategoryName_id = category_id.id, Description= Description)
                    new_operation.save()
                
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new Category has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to add Operation',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_operations':
                if request.user.has_perm('APEN.change_operations'):
                # Get all data from the request
                    id = request.POST.get('id')
                    operations = request.POST.get('OperationName')
                    CategoryName = request.POST.get('CategoryName')
                    Description = request.POST.get('Description')
                        
                    # Validaet data
                    if operations == '' or operations == 'null' or operations is None or operations == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Operation ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
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

                    category = OperationCategory.objects.get(id=CategoryName)
                    update_operation= Operations.objects.get(id=id)
                    update_operation.OperationName = operations
                    update_operation.CategoryName = category
                    update_operation.Description = Description
                    
                    update_operation.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'an Operation Category has been updated',
                                'title': 'masha allah !' + CategoryName + " been updated" ,
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to update Operations',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getOperations":
                if request.user.has_perm('APEN.change_operations'):
                    id = request.POST.get('id')
                    operation_id = Operations.objects.get(id = id)
                    message = {
                        'id': operation_id.id,
                        'Operation': operation_id.OperationName,
                        'CategoryName': operation_id.CategoryName.id,
                        'Description': operation_id.Description,
                        
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
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