from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from  .views import *
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re
@login_required(login_url='Login')
def view_all_prerequirements(request):
    try:
        if request.user.has_perm('Hr.Approve_employee'):
            context = {
                'all_jobtypes': JobType.objects.all(),
                'departments': Departments.objects.all(),
                'directarate_all': Directorate.objects.all(),
            }
            return render(request, "Hr/prequirements.html", context)
        else:
             return render(request, "Hr/403.html")
            
    except Exception as error:
        username = request.user.has_username
        name = request.user.has_first_name + ' ' + request.user.has_last_name
        sendException(
            request, username, name, error)
        context = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return render(request, "Hr/500.html", context)


@login_required(login_url='Login')
def manage_requirements(request, action):
    try:
        if request.method == "POST":
            if action == 'new_jobtype':
                if request.user.has_perm('Hr.add_jobtype'):
                    job_type_name = request.POST.get('job_type_name')
                    descriptions = request.POST.get('descriptions')
                    relateAppoint = request.POST.get('relateAppoint')

                    if job_type_name == '' or job_type_name == 'null' or job_type_name is None or job_type_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job type name' + job_type_name + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(job_type_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job type name' + job_type_name + "not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + job_type_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  decription  jobtype',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    job_type_name = RemoveSpecialCharacters(job_type_name)
                    descriptions = RemoveSpecialCharacters(descriptions)

                    if JobType.objects.filter(name = job_type_name).exists():
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job type name: ' + job_type_name + ", is ixisted",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                            

                    job_type = JobType(name=job_type_name,
                                    description=descriptions,is_appoitment_rel = relateAppoint)
                    job_type.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new jobtype called {job_type_name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to add job',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_job_types':
                if request.user.has_perm('Hr.change_jobtype'):
                    # Get all data from the request
                    job_type_name = request.POST.get('job_type_name')
                    descriptions = request.POST.get('descriptions')
                    relateAppoint = request.POST.get('relateAppoint')

                    id = request.POST.get('id')

                    # Validaet data
                    if job_type_name == '' or job_type_name == 'null' or job_type_name is None or job_type_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job type name' + job_type_name ,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if text_validation(job_type_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job type name' + job_type_name + "not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    else:
                        RemoveSpecialCharacters(job_type_name)

                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + job_type_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  decription  jobtype',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    job_type_name = RemoveSpecialCharacters(job_type_name)
                    descriptions = RemoveSpecialCharacters(descriptions)



                    update_job_type_single = JobType.objects.get(id=id)
                    update_job_type_single.name = job_type_name
                    update_job_type_single.description = descriptions
                    update_job_type_single.is_appoitment_rel = relateAppoint
                    update_job_type_single.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': ' job type has been updated',
                            'title': "re bank up[dated]",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to change job',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_job_single_Data":
               if request.user.has_perm('Hr.view_jobtype'):
                    id = request.POST.get('id')
                    get_jobtype_single = JobType.objects.get(
                        id=id)

                    message = {
                        'id': get_jobtype_single.id,
                        'name': get_jobtype_single.name,
                        'discription': get_jobtype_single.description,
                        'is_related': get_jobtype_single.is_appoitment_rel,
                                
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
               else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to view job',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getjobtypeData":
                if request.user.has_perm('Hr.view_jobtype'):

                    single_job_type = JobType.objects.all()
                    message = []
                    for xjobtype in range(0, len(single_job_type)):
                        message.append({
                            'id': single_job_type[xjobtype].id,
                            'name': single_job_type[xjobtype].name,
                            'discription': single_job_type[xjobtype].description,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to view job',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
    # Title

            if action == 'new_title':     
              if request.user.has_perm('Hr.add_title'):        
                title_name = request.POST.get('title_names')
                descriptions = request.POST.get('title_dis')


                if title_name == '' or title_name == 'null' or title_name is None or title_name == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter job titlename' + title_name + "",
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if text_validation(title_name) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter job title name' + title_name + "not valid name",
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'provide description for ' + title_name,
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if text_validation(descriptions) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': f'Please enter text only for  decription  {title_name}',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                title_name = RemoveSpecialCharacters(title_name)
                descriptions = RemoveSpecialCharacters(descriptions)
                if Title.objects.filter(name = title_name).exists():
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'title name: ' + title_name + ", is existed",
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                save_title = Title(name=title_name,
                                description=descriptions )
                save_title.save()

                return JsonResponse(
                    {
                        'isError': False,
                        'Message': f'new title called {title_name}  has been created',
                        'title': 'successful created!',
                        'type': 'success',
                    }
                )
              else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to Add title',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_title':
                 if request.user.has_perm('Hr.change_title'):
                    # Get all data from the request
                    id = request.POST.get('id')
                    title_name = request.POST.get('title_names')
                    descriptions = request.POST.get('title_dis')


                    if title_name == '' or title_name == 'null' or title_name is None or title_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job titlename' + title_name + "",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(title_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter job title name' + title_name + "not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + title_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': f'Please enter text only for  decription  {title_name}',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    title_name = RemoveSpecialCharacters(title_name)
                    descriptions = RemoveSpecialCharacters(descriptions)



                    update_title = Title.objects.get(id=id)
                    update_title.name = title_name
                    update_title.description = descriptions            
                    update_title.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f' {title_name} has been updated',
                            'title': "updated successfully",
                            'type': 'success',
                        }
                    )
                 else:
                     return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to Change title',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_single_title":
                if request.user.has_perm('Hr.view_title'):  
                    id = request.POST.get('id')
                    get_single_title = Title.objects.get(
                        id=id)

                    message = {
                        'id': get_single_title.id,
                        'name': get_single_title.name,
                        'discription': get_single_title.description,
                
                                
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to view Title',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_all_titles":
                if request.user.has_perm('Hr.view_title'):  

                    all_title = Title.objects.all()
                    message = []
                    for xtitle in range(0, len(all_title)):
                        message.append({
                            'id': all_title[xtitle].id,
                            'name': all_title[xtitle].name,
                            'discription': all_title[xtitle].description,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to view Title',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
    # Secretary

            if action == 'new_secretory':
                if request.user.has_perm('Hr.add_secretary'):   
                    director_name = request.POST.get('director_name')
                    secretary_name = request.POST.get('secretary_name')
                    descriptions = request.POST.get('descriptions_director')
                    if director_name == '' or director_name == 'null' or director_name is None or director_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Select Director Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if secretary_name == '' or secretary_name == 'null' or secretary_name is None or secretary_name == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please write Secretary Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )


                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + secretary_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  decription  Jobtitle',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                
                    if Secretary.objects.filter(name = secretary_name).exists():
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'this: ' + secretary_name + ", is ixisted",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    secretary_name = RemoveSpecialCharacters(secretary_name)
                    descriptions = RemoveSpecialCharacters(descriptions)
                        
                    save_secretary = Secretary(name = secretary_name, director_id = director_name, Discriptions = descriptions)
                    save_secretary.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new secretary called {secretary_name} is been created',
                            'title': 'Successfully!',
                            'type': 'success',
                        } )
                else:
                     return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to Add Secretary',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )            
            if action == 'update_secretary':
                if request.user.has_perm('Hr.change_secretary'):                 
                    id = request.POST.get('id')
                    # Get all data from the request
                    director_name = request.POST.get('director_name')
                    secretary_name = request.POST.get('secretary_name')
                    descriptions = request.POST.get('descriptions_director')

                    if director_name == '' or director_name == 'null' or director_name is None or director_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Select Director Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if secretary_name == '' or secretary_name == 'null' or secretary_name is None or secretary_name == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please write Secretary Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )


                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + secretary_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  decription  secretaroy',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                
                    update_secretary = Secretary.objects.get(id=id)
                    update_secretary.name = director_name
                    update_secretary.name = secretary_name
                    update_secretary.Discriptions = descriptions
                    update_secretary.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'secretary: {secretary_name} is  updated ',
                            'title': "Successfully",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to Change Secretary',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_secretary_data":
                if request.user.has_perm('Hr.view_secretary'):   
                    id = request.POST.get('id')
                    getSingleSecretory = Secretary.objects.get(
                        id=id)

                    message = {
                        'id': getSingleSecretory.id,
                        'director': getSingleSecretory.director.id,
                        'secretory': getSingleSecretory.name,
                        'discription': getSingleSecretory.Discriptions,


                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No  Permission to get secretary data',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getSecretaryData":
                if request.user.has_perm('Hr.view_secretary'):      
                    getSecretary = Secretary.objects.all()
                    message = []
                    for xsecretary in range(0, len(getSecretary)):
                        message.append({
                            'id': getSecretary[xsecretary].id,
                            'secretary': getSecretary[xsecretary].name,
                            'director': getSecretary[xsecretary].director.name,
                            'discription': getSecretary[xsecretary].Discriptions,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to get secretary data',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )


#  Departments
            if action == 'new_Department':
                if request.user.has_perm('Hr.add_departments'):   
                    departments_name = request.POST.get('Department_name')
                    descriptions = request.POST.get('department_descriptions')
                    director_id = request.POST.get('director_id')

                    if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Director name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if departments_name == '' or departments_name == 'null' or departments_name is None or departments_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Department name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if text_validation(departments_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  department name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + departments_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  department descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    descriptions = RemoveSpecialCharacters(descriptions)

                    hospital_departments = Departments(
                    director_id = director_id,  department_name=departments_name, description=descriptions)
                    hospital_departments.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new department called {departments_name}  is been created',
                            'title': 'Successfully!',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to add Department',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_departments':
                if request.user.has_perm('Hr.change_departments'):
                    # Get all data from the request
                    departments_name = request.POST.get('Department_name')
                    descriptions = request.POST.get('department_descriptions')
                    id = request.POST.get('id')

                    # Validaet data
                    if departments_name == '' or departments_name == 'null' or departments_name is None or departments_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Department name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(departments_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  department name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + departments_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  department descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_departments = Departments.objects.get(id=id)

                    update_departments.department_name = departments_name
                    update_departments.description = descriptions
                    update_departments.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'Department of ({departments_name}) is  updated ',
                            'title': "Successfully",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to change department',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_Department_single_Data":     
                if request.user.has_perm('Hr.view_departments'):
                    id = request.POST.get('id')
                    get_department_single_data = Departments.objects.get(
                        id=id)

                    message = {
                        'id': get_department_single_data.id,
                        'director': get_department_single_data.director.id,
                        'department_name': get_department_single_data.department_name,
                        'department_discription': get_department_single_data.description,


                      }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Permission to change department',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getDepartmentData":               
               if request.user.has_perm('Hr.view_departments'):
                    single_department = Departments.objects.all()
                    message = []
                    for xdepartment in range(0, len(single_department)):
                        message.append({
                            'id': single_department[xdepartment].id,
                            
                            'director_name': single_department[xdepartment].director.name,
                            'department_name': single_department[xdepartment].department_name,
                            'department_discription': single_department[xdepartment].description,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
               else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
 #  Work shift
            if action == 'new_workshift':  
                if request.user.has_perm('Hr.add_work_shift'):               
                    departmentsID = request.POST.get('departments')
                    shift_name = request.POST.get('shift_name')
                    shiftType = request.POST.get('shiftType')
                    shift_day = request.POST.get('shift_day')
                    shift_start_time = request.POST.get('shift_start_time')
                    shift_end_time = request.POST.get('shift_end_time')

                    if shift_name == '' or shiftType == 'null' or shiftType is None or shiftType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter shift name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(shift_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  shift name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shiftType == '' or shiftType == 'null' or shiftType is None or shiftType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide shiftType for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shift_day == '' or shift_day == 'null' or shift_day is None or shift_day == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide shiftType for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shift_start_time == '' or shift_start_time == 'null' or shift_start_time is None or shift_start_time == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide start time for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shift_end_time == '' or shift_end_time == 'null' or shift_end_time is None or shift_end_time == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide end time for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    hospital_work_shift = Work_shift(shift_name=shift_name, shift_date=shift_day,
                                                    shift_type=shiftType, start_time=shift_start_time, end_time=shift_end_time ,department_id = departmentsID )
                    hospital_work_shift.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new  {shift_name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_workshift':
                if request.user.has_perm('Hr.change_work_shift'): 
                    # Get all data from the request
                    shift_name = request.POST.get('shift_name')
                    shiftType = request.POST.get('shiftType')
                    shift_day = request.POST.get('shift_day')
                    shift_start_time = request.POST.get('shift_start_time')
                    shift_end_time = request.POST.get('shift_end_time')
                    id = request.POST.get('id')

                    # Validaet data

                    if shift_name == '' or shiftType == 'null' or shiftType is None or shiftType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter shift name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(shift_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  shift name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shiftType == '' or shiftType == 'null' or shiftType is None or shiftType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide shiftType for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if shift_day == '' or shift_day == 'null' or shift_day is None or shift_day == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide shiftType for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if shift_start_time == '' or shift_start_time == 'null' or shift_start_time is None or shift_start_time == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide start time for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if shift_end_time == '' or shift_end_time == 'null' or shift_end_time is None or shift_end_time == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide end time for ' + shift_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_working_shift = Work_shift.objects.get(id=id)

                    update_working_shift.shift_name = shift_name
                    update_working_shift.shift_date = shift_day
                    update_working_shift.shift_type = shiftType
                    update_working_shift.start_time = shift_start_time
                    update_working_shift.end_time = shift_end_time
                    update_working_shift.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f' {shift_name} updated ',
                            'title': "",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
          
            if action == "get_workshift_single_Data":
                 if request.user.has_perm('Hr.view_work_shift'):
                    id = request.POST.get('id')
                    get_workshift_single_data = Work_shift.objects.get(
                        id=id)
                   
                    message = {

                        'id': get_workshift_single_data.id,
                        'departments': get_workshift_single_data.department.id,
                        'shift_name': get_workshift_single_data.shift_name,
                        'shift_days': get_workshift_single_data.shift_date,
                        'shifttype': get_workshift_single_data.shift_type,
                        'shift_start_time': get_workshift_single_data.start_time,
                        'shift_end_time': get_workshift_single_data.end_time,

                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                 else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getworkshifttData":        
                    creteshifts = Work_shift.objects.all()
                    message = []
                    for xworkshift in range(0, len(creteshifts)):
                        message.append({
                            'id': creteshifts[xworkshift].id,
                            'departments': creteshifts[xworkshift].department.department_name,
                            'shift_name': creteshifts[xworkshift].shift_name,
                            'shift_type': creteshifts[xworkshift].shift_type,
                            'shift_days': creteshifts[xworkshift].shift_date,
                            'shift_start_day': creteshifts[xworkshift].start_time,
                            'shift_end_day': creteshifts[xworkshift].end_time,
                            'url': creteshifts[xworkshift].get_absolute_url(),


                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

# Banks

            if action == 'new_Banks':
                 if request.user.has_perm('Hr.add_banks'):
                    Bank_name = request.POST.get('Bank_name')
                    Bank_descriptions = request.POST.get('Bank_descriptions')

                    if Bank_name == '' or Bank_name == 'null' or Bank_name is None or Bank_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Bank_name ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Bank_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  bank name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Bank_descriptions == '' or Bank_descriptions == 'null' or Bank_descriptions is None or Bank_descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + Bank_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Bank_descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  bank descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    bank_is_existed = Banks.objects.filter(name=Bank_name)
                    if bank_is_existed:
                        bank_is_belong_to = Banks.objects.get(name=Bank_name)
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': f'bank {Bank_name} is existed ({bank_is_belong_to.name})',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    Bank_saving = Banks(
                        name=Bank_name, description=Bank_descriptions)
                    Bank_saving.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new Bank called {Bank_name}  has been created',
                            'title': 'completed Success!',
                            'icon': "success",
                            'type': 'success',
                        }
                    )
                 else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'update_Bank_data':
               if request.user.has_perm('Hr.change_banks'):  
                    # Get all data from the request
                    Bank_name = request.POST.get('Bank_name')
                    Bank_descriptions = request.POST.get('Bank_descriptions')
                    id = request.POST.get('id')

                    # Validaet data

                    if Bank_name == '' or Bank_name == 'null' or Bank_name is None or Bank_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Bank_name ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Bank_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  bank name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Bank_descriptions == '' or Bank_descriptions == 'null' or Bank_descriptions is None or Bank_descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + Bank_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(Bank_descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for  bank descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_bank = Banks.objects.get(id=id)

                    update_bank.name = Bank_name
                    update_bank.description = Bank_descriptions
                    update_bank.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'{Bank_name} is updated ',
                            'title': "Successfuly Updated",
                            'type': 'success',
                        }
                    )
               else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_single_banks_Data":
                if request.user.has_perm('Hr.view_banks'):
                    id = request.POST.get('id')
                    get_single_bank_data = Banks.objects.get(
                        id=id)

                    message = {
                        'id': get_single_bank_data.id,
                        'Bank_name': get_single_bank_data.name,
                        'bank_discription': get_single_bank_data.description,


                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getAllBanksData":
                if request.user.has_perm('Hr.add_banks'):

                    all_banks = Banks.objects.all()
                    message = []
                    for xdepartment in range(0, len(all_banks)):
                        message.append({

                            'id': all_banks[xdepartment].id,
                            'Bank_name': all_banks[xdepartment].name,
                            'Banks_descriptions': all_banks[xdepartment].description,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
# Salary

            if action == 'New_Salary':
                if request.user.has_perm('Hr.add_salary'):     
                    jobtype_salary = request.POST.get('jobtype_salary')
                    base_salary = request.POST.get('base_salary')
                    name = request.POST.get('name')


                    if jobtype_salary == '' or jobtype_salary == 'null' or jobtype_salary is None or jobtype_salary == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Job type ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  Salary name for ' + jobtype_salary,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(name):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide only text for  salary name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if base_salary == '' or base_salary == 'null' or base_salary is None or base_salary == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide base Salary for ' + jobtype_salary,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not number_validation(base_salary):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide only number for  base salary',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )


                
                    salary_saving = Salary(
                        base_salary=base_salary, job_type_id=jobtype_salary, name = name )
                    salary_saving.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'new Base Salery is being created',
                            'title': 'completed Success!',
                            'icon': "success",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'Update_Salary_data':
                 if request.user.has_perm('Hr.change_salary'):
                    # Get all data from the request
                    jobtype_salary = request.POST.get('jobtype_salary')
                    name = request.POST.get('name')

                    base_salary = request.POST.get('base_salary')             
                    id = request.POST.get('id')

                    # Validaet data
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter salary name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    # if not validate_text_only(name):
                    #     return JsonResponse(
                    #         {
                    #             'isError': True,
                    #             'Message': 'provide only text for salary Name',
                    #             'title': 'Validation Error!',
                    #             'type': 'warning',
                    #         }
                    #     )
                    if jobtype_salary == '' or jobtype_salary == 'null' or jobtype_salary is None or jobtype_salary == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Department name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if base_salary == '' or base_salary == 'null' or base_salary is None or base_salary == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide base Salary for ' + jobtype_salary,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not number_validation(base_salary):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide only number for  base salary',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                
                    name = RemoveSpecialCharacters(name)
                    single_job_type = JobType.objects.get(id=jobtype_salary)
                    update_base_salary = Salary.objects.get(id=id)

                    update_base_salary.job_type = single_job_type
                    update_base_salary.base_salary = base_salary                
                    update_base_salary.name = name                
                    update_base_salary.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f' {update_base_salary.job_type.name} updated ',
                            'title': "Successfuly Updated",
                            'type': 'success',
                        }
                    )
                 else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )    
            if action == "get_single_Salary_Data":
                if request.user.has_perm('Hr.view_salary'):
                    id = request.POST.get('id')
                    single_salary_jobtype = Salary.objects.get(
                        id=id)

                    message = {
                        'id': single_salary_jobtype.id,
                        'jobtype_salary': single_salary_jobtype.job_type.id,
                        'jobtype_salary_name': single_salary_jobtype.job_type.name,
                        'base_salry': single_salary_jobtype.base_salary,             
                        'name': single_salary_jobtype.name,


                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getAllSalaryData":
                if request.user.has_perm('Hr.view_salary'):
                    single_base_salary = Salary.objects.all()
                    message = []
                    for xbase_salary in range(0, len(single_base_salary)):
                        message.append({

                            'id': single_base_salary[xbase_salary].id,
                            'jobtype': single_base_salary[xbase_salary].job_type.name,
                            'base_salary': single_base_salary[xbase_salary].base_salary,
                            'fix_allow': single_base_salary[xbase_salary].fixed_allow,
                            'name': single_base_salary[xbase_salary].name,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
                
# Department Section

            if action == 'New_section':
                if request.user.has_perm('Hr.add_depart_sections'):
                    depart_ID = request.POST.get('depart_ID')
                    section_name = request.POST.get('section_name')

                    if depart_ID == '' or depart_ID == 'null' or depart_ID is None or depart_ID == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Department ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if section_name == '' or section_name == 'null' or section_name is None or section_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide section for  ' + depart_ID,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(section_name):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide text only for  section name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    section_name = RemoveSpecialCharacters(section_name)
                    get_department = Departments.objects.get(id=depart_ID)
                    save_sections = Depart_Sections(
                        departments=get_department, department_sections=section_name)
                    save_sections.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new Section {section_name} is being created',
                            'title': 'completed Success!',
                            'icon': "success",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'Update_section_data':
                if request.user.has_perm('Hr.change_depart_sections'):
                    # Get all data from the request
                    depart_ID = request.POST.get('depart_ID')
                    section_name = request.POST.get('section_name')
                    id = request.POST.get('id')

                    # Validaet data
                    if depart_ID == '' or depart_ID == 'null' or depart_ID is None or depart_ID == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Department ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if section_name == '' or section_name == 'null' or section_name is None or section_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide section for  ' + depart_ID,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(section_name):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide text only for  section name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    section_name = RemoveSpecialCharacters(section_name)
                    get_single_depart = Departments.objects.get(id=depart_ID)
                    update_section = Depart_Sections.objects.get(id=id)

                    update_section.departments = get_single_depart
                    update_section.department_sections = section_name
                    update_section.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'Section of {update_section.department_sections} is updated ',
                            'title': "Successfuly ",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_single_section_Data":
                if request.user.has_perm('Hr.view_depart_sections'):
                    id = request.POST.get('id')
                    single_section_jobtype = Depart_Sections.objects.get(id=id)

                    message = {
                        'id': single_section_jobtype.id,
                        'department': single_section_jobtype.departments.id,
                        'department_sections': single_section_jobtype.department_sections,



                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "getSectionData":             
                if request.user.has_perm('Hr.view_depart_sections'):
                    get_section_data = Depart_Sections.objects.all()
                    message = []
                    for xsections in range(0, len(get_section_data)):
                        message.append({

                            'id': get_section_data[xsections].id,
                            'department': get_section_data[xsections].departments.department_name,
                            'section_name': get_section_data[xsections].department_sections,


                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
# Specializations

            if action == 'new_administarator':
                if request.user.has_perm('Hr.add_directorate'):
                    administrator = request.POST.get('spec_name')
                    descriptions = request.POST.get('description_spec')

                    if administrator == '' or administrator == 'null' or administrator is None or administrator == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Specialation Name ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(administrator):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  text only for administrator name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + administrator,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(descriptions):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  text only for administrator descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    administrator = RemoveSpecialCharacters(administrator)
                    descriptions = RemoveSpecialCharacters(descriptions)
                    save_administrator = Directorate(
                        name = administrator, Discriptions=descriptions)
                    save_administrator.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'new administrator is being created',
                            'title': 'completed Success!',
                            'icon': "success",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'Update_specialization_data':
                if request.user.has_perm('Hr.change_directorate'):
                    # Get all data from the request
                    id = request.POST.get('id')
                    administrator = request.POST.get('spec_name')
                    descriptions = request.POST.get('description_spec')

                    if administrator == '' or administrator == 'null' or administrator is None or administrator == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Specialation Name ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(administrator):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  text only for administrator name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if descriptions == '' or descriptions == 'null' or descriptions is None or descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + administrator,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if not text_validation(descriptions):
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  text only for administrator descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide  text only for specialization descriptions',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    edit_specializatin = Directorate.objects.get(id=id)
                    edit_specializatin.name = administrator
                    edit_specializatin.Discriptions = descriptions
                    edit_specializatin.save()
                    
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'{administrator} is updated ',
                            'title': "Successfuly Updated",
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_single_specialization_Data":    
                if request.user.has_perm('Hr.view_directorate'):             
                    id = request.POST.get('id')
                    get_single_specialization = Directorate.objects.get(id=id)
                    message = {

                    'id': get_single_specialization.id,
                    'specialization_name': get_single_specialization.name,
                    'description': get_single_specialization.Discriptions,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_doctor_Specialization":
                if request.user.has_perm('Hr.view_directorate'):  
                    all_specialization = Directorate.objects.all()
                    message = []
                    for xspecilization in range(0, len(all_specialization)):
                        message.append({

                            'id': all_specialization[xspecilization].id,
                            'specialization_name': all_specialization[xspecilization].name,
                            'description': all_specialization[xspecilization].Discriptions,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'No Access Permission',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )    
    except Exception as error:
        username = request.user.has_username
        name = request.user.has_first_name + ' ' + request.user.has_last_name
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
def hrmReportview(request):
    return render(request, 'Hr/hrmreport.html')