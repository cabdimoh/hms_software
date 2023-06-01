from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from  .views import *
from .models import *
# from  APEN.models import Specialities

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re



@login_required(login_url='Login')
def manage_Qualification(request, action):
    try:
        if request.method == "POST":
            if action == 'new_qualification':
                if request.user.has_perm('Hr.add_qualification'):
                    # Get all data from the request
                    employee_id = request.POST.get('employee_id')
                    name = request.POST.get('name')
                    specialization = request.POST.get('specialization')

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

                    # Validaet data
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Qualification name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for qualification name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if specialization == '' or specialization == 'null' or specialization is None or specialization == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter specialization name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(specialization) == False:

                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for specialization name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    # getting employee instance
                    name = RemoveSpecialCharacters(name)
                    specialization = RemoveSpecialCharacters(specialization)

                    get_employee = Employee.objects.get(id=employee_id)

                    qualification = Qualification(
                        employee=get_employee, name=name, Specialization=specialization, Documents=file)
                    qualification.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New qualification has been created',
                            'title': 'success!',
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

            if action == 'update_qualification':
                if request.user.has_perm('Hr.change_qualification'):
                    # Get all data from the request
                    id = request.POST.get('id')
                    name = request.POST.get('name')
                    specialization = request.POST.get('specialization')
                    # Validaet data
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Qualification name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for qualification name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if specialization == '' or specialization == 'null' or specialization is None or specialization == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter specialization name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(specialization) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for specialization name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_qualification = Qualification.objects.get(
                        id=id)
                    update_qualification.name = name
                    update_qualification.Specialization = specialization
                    update_qualification.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'qualification employee has been updated',
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
            if action == 'update_qualification_document':
                if request.user.has_perm('Hr.change_qualification'):
                    # Get all data from the request

                    id = request.POST.get('id')

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

                    update_qualification = Qualification.objects.get(
                        id=id)
                    update_qualification.Documents = file
                    update_qualification.save()
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
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if action == "getData":
                if request.user.has_perm('Hr.view_qualification'):
                    id = request.POST.get('id')
                    getqualification = Qualification.objects.get(
                        id=id)

                    message = {
                        'id': getqualification.id,
                        'name': getqualification.name,
                        'specialization': getqualification.Specialization,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if action == "getAllData":
                if request.user.has_perm('Hr.view_qualification'):
                    id = request.POST.get('id')
                    getqualification = Qualification.objects.filter(
                        employee=id)
                    message = []
                    for xqualification in range(0, len(getqualification)):
                        message.append({

                            'id': getqualification[xqualification].id,
                            'name': getqualification[xqualification].name,
                            'specialization': getqualification[xqualification].Specialization,
                            'document': getqualification[xqualification].get_document_detail()

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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)

    # fetch




# Experience
@login_required(login_url='Login')
def manage_Experience(request, action):
    try:
        if request.method == "POST":
            if action == 'new_Experience':
                if request.user.has_perm('Hr.add_experience'):
                    # Get all data from the request
                    employee_id = request.POST.get('employee_id')
                    name = request.POST.get('name_exp')
                    place_exp = request.POST.get('place_exp')
                    start_day_exp = request.POST.get('start_time_exp')
                    end_day_exp = request.POST.get('end_time_exp')



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

                    # Validaet data
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Experience name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for Experience name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if place_exp == '' or place_exp == 'null' or place_exp is None or place_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter place of Experience',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if start_day_exp == '' or start_day_exp == 'null' or start_day_exp is None or start_day_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter start day',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if end_day_exp == '' or end_day_exp == 'null' or end_day_exp is None or end_day_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter last day plac',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if end_day_exp < start_day_exp:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter valid date. End date is behind start day',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )  

                    # getting employee instance
                    name = RemoveSpecialCharacters(name)
                    place_exp = RemoveSpecialCharacters(place_exp)
                    get_employee = Employee.objects.get(id=employee_id)

                    qualification = Experience(
                        employee=get_employee, name=name,place =place_exp,start = start_day_exp,end =end_day_exp , documents=file)
                    qualification.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'new Experience has been created',
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
            if action == 'update_Experience':
                if request.user.has_perm('Hr.change_experience'):
                    # Get all data from the request
                    name = request.POST.get('name_exp')
                    place_exp = request.POST.get('place_exp')
                    start_day_exp = request.POST.get('start_time_exp')
                    end_day_exp = request.POST.get('end_time_exp')
                    id = request.POST.get('id')


                    # Validaet data
                    if name == '' or name == 'null' or name is None or name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Experience name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for Experience name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if place_exp == '' or place_exp == 'null' or place_exp is None or place_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter place of Experience',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(place_exp) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for Experience place',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if start_day_exp == '' or start_day_exp == 'null' or start_day_exp is None or start_day_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter start day',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if end_day_exp == '' or end_day_exp == 'null' or end_day_exp is None or end_day_exp == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter last day plac',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    

                    update_qualification = Experience.objects.get(
                        id=id)
                    update_qualification.name = name
                    update_qualification.place = place_exp
                    update_qualification.start = start_day_exp
                    update_qualification.end = end_day_exp
                    update_qualification.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'Experience has been updated',
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
            if action == 'update_Experience_document':
                if request.user.has_perm('Hr.change_experience'):
                    # Get all data from the request
                    id = request.POST.get('id')

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

                    update_qualification = Experience.objects.get(
                        id=id)
                    update_qualification.documents = file
                    update_qualification.save()
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
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if action == "getSingleExpirience":
                if request.user.has_perm('Hr.view_experience'):
                    id = request.POST.get('id')
                    getExperience = Experience.objects.get(
                        id=id)

                    message = {
                        'id': getExperience.id,
                        'name': getExperience.name,
                        'place': getExperience.place,
                        'start': getExperience.start,
                        'end': getExperience.end,
                    
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    })
            if action == "getExperienceData":    
                if request.user.has_perm('Hr.view_experience'):            
                    id = request.POST.get('id')
                    getExperience = Experience.objects.filter(
                        employee=id)
                    message = []
                    for xexperience in range(0, len(getExperience)):
                        message.append({

                            'id': getExperience[xexperience].id,
                            'name': getExperience[xexperience].name,
                            'place': getExperience[xexperience].place,
                            'start': getExperience[xexperience].start,
                            'end': getExperience[xexperience].end,
                            'document': getExperience[xexperience].get_document_detail()

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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)

# JobDetails
@login_required(login_url='Login')
def manage_JobDetail(request, action):
    try:      
        if request.method == "POST":
            if action == 'new_JobDetail':
              
                if request.user.has_perm('Hr.add_jobdetails'):    
                    # Get all data from the request
                    employee_id = request.POST.get('employee_id')
                    job_type = request.POST.get('job_type')
                    empl_type = request.POST.get('empl_type')
                    depart_id = request.POST.get('depart_id')
                    depart_section = request.POST.get('section_id')
                    director_id = request.POST.get('directorate_id')
                    secretary_id = request.POST.get('secretory_id')
                    salary = request.POST.get('Jobtype_Salary')
                    fix_alowence = request.POST.get('fix_alowence')

                    # Validate data

                    if job_type == '' or job_type == 'null' or job_type is None or job_type == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'what is your job type ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if empl_type == '' or empl_type == 'null' or empl_type is None or empl_type == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Type of Employee',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if salary == '' or salary == 'null' or salary is None or salary == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Where is Salary',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if fix_alowence == '' or fix_alowence == 'null' or fix_alowence is None or fix_alowence == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Where is Allowance',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )


                    

                    get_employee = Employee.objects.get(id=employee_id) 
                    sin_job_types = JobType.objects.get(id=job_type)           
                    salaryi = Salary.objects.get(id=salary)             

                    if empl_type == "General-Director":
                        get_depart_section = None
                        get_secretary_id = None
                        sin_department = None
                        if Directorate.objects.filter(id= director_id).exists():
                            get_director_id = Directorate.objects.get(id= director_id)  
                            if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                    return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Choose Director Name',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                ) 
                
                    if empl_type == "Director-Secretory":
                        get_depart_section = None                    
                        sin_department = None
                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if secretary_id == '' or secretary_id == 'null' or secretary_id is None or secretary_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director secretary Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_secretary_id = Secretary.objects.get(id= secretary_id)  
                    
                    if empl_type == "Department-Head":
                        get_depart_section = None                    
                        sin_department = None
                        get_secretary_id = None
                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  

                    if empl_type == "Section-Head":
                        get_secretary_id = None                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  


                        if depart_section == '' or depart_section == 'null' or depart_section is None or depart_section == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department Section',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_depart_section = Depart_Sections.objects.get(id= depart_section)  
                    if empl_type == "Employee":
                        get_secretary_id = None                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  


                        if depart_section == '' or depart_section == 'null' or depart_section is None or depart_section == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department Section',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_depart_section = Depart_Sections.objects.get(id= depart_section)  
                    
                    if salaryi:
                        salaryi.fixed_allow = fix_alowence
                        salaryi.save()
                    
                    total_salary = float(salaryi.fixed_allow) + float(salaryi.base_salary)
                    
            
                    job_detail = JobDetails(
                        employee=get_employee,
                        job_type=sin_job_types,
                        department_all=sin_department,
                        director = get_director_id,
                        secretory = get_secretary_id,
                        employee_type=empl_type,
                        salary=salaryi,
                        depar_section=get_depart_section,
                        base_pay = total_salary
                    
                    
                        )
                    job_detail.save()
                    return JsonResponse(
                        {

                            'isError': False,
                            'Message': 'new job detail has been created',
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

                    },
                )


            if action == 'update_JobDetail':
                if request.user.has_perm('Hr.change_jobdetails'):
                    # Get all data from the request
                    employee_id = request.POST.get('employee_id')
                    job_type = request.POST.get('job_type')
                    empl_type = request.POST.get('empl_type')
                    depart_id = request.POST.get('depart_id')
                    depart_section = request.POST.get('section_id')
                    director_id = request.POST.get('directorate_id')
                    secretary_id = request.POST.get('secretory_id')
                    salary = request.POST.get('Jobtype_Salary')
                    fix_alowence = request.POST.get('fix_alowence')
                    id = request.POST.get('id')

                    # Validaet data
                    if job_type == '' or job_type == 'null' or job_type is None or job_type == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose job type ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if empl_type == '' or empl_type == 'null' or empl_type is None or empl_type == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose  Employee Type',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if fix_alowence == '' or fix_alowence == 'null' or fix_alowence is None or fix_alowence == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Write Allawance',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )


                    get_employee = Employee.objects.get(id=employee_id) 
                    sin_job_types = JobType.objects.get(id=job_type)           
                    salaryi = Salary.objects.get(id=salary)             

                    if empl_type == "General-Director":
                        get_depart_section = None
                        get_secretary_id = None
                        sin_department = None
                        if Directorate.objects.filter(id= director_id).exists():
                            get_director_id = Directorate.objects.get(id= director_id)  
                            if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                    return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Choose Director Name',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                ) 
                
                    if empl_type == "Director-Secretory":
                        get_depart_section = None                    
                        sin_department = None
                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if secretary_id == '' or secretary_id == 'null' or secretary_id is None or secretary_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director secretary Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_secretary_id = Secretary.objects.get(id= secretary_id)  
                    
                    if empl_type == "Department-Head":
                        get_depart_section = None                    
                        sin_department = None
                        get_secretary_id = None
                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Where is allowance',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  

                    if empl_type == "Section-Head":
                        get_secretary_id = None                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  


                        if depart_section == '' or depart_section == 'null' or depart_section is None or depart_section == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department Section',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_depart_section = Depart_Sections.objects.get(id= depart_section)  
                  
                    if empl_type == "Employee":
                        get_secretary_id = None                        
                        if director_id == '' or director_id == 'null' or director_id is None or director_id == 'undefined':
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Director Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_director_id = Directorate.objects.get(id= director_id)  
                    
                        if depart_id == '' or depart_id == 'null' or depart_id is None or depart_id == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        sin_department = Departments.objects.get(id= depart_id)  


                        if depart_section == '' or depart_section == 'null' or depart_section is None or depart_section == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Choose Department Section',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        get_depart_section = Depart_Sections.objects.get(id= depart_section)  
                    
                    update_jobDetail = JobDetails.objects.get(id=id)
                    update_jobDetail.base_pay = 0

                    if salaryi:
                        salaryi.fixed_allow = fix_alowence
                        salaryi.save()
                    

                    total_salary = float(salaryi.fixed_allow) + float(salaryi.base_salary)
                   
            

                    get_jobtype = JobType.objects.get(id=job_type)
                    get_salary = Salary.objects.get(id=salary)
                


                    jobDetailbase = JobDetails.objects.get(id=id)
                    jobDetailbase.base_pay = get_salary.base_salary + get_salary.fixed_allow
                    base_salary = jobDetailbase.base_pay

                    update_jobDetail.director = get_director_id
                    update_jobDetail.secretory = get_secretary_id
                    update_jobDetail.job_type = get_jobtype
                    update_jobDetail.employee_type = empl_type
                    update_jobDetail.department_all = sin_department
                    update_jobDetail.base_pay = base_salary
                    update_jobDetail.depar_section = get_depart_section
                    update_jobDetail.salary = get_salary             
                    update_jobDetail.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'{update_jobDetail.employee.first_name} job has been updated',
                            'title': 'successfully!' + update_jobDetail.employee.first_name + "Job detail been updated",
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

                    },
                )
                
            if action == "getData":
                if request.user.has_perm('Hr.view_jobdetails'):
                    id = request.POST.get('id')
                    depart_section = request.POST.get('section_id')
                    getJobDetail = JobDetails.objects.get(
                        id=id)

                    message = {
                        'id': getJobDetail.id,
                        'job_type': getJobDetail.job_type.id,
                        'director': getJobDetail.director.id,
                        'secretary':'null' if getJobDetail.secretory== None else getJobDetail.secretory.id,
                        'department':'null' if getJobDetail.department_all== None else getJobDetail.department_all.id,
                        'department_section':'null' if getJobDetail.depar_section == None else getJobDetail.depar_section.id,
                        'employee_type': getJobDetail.employee_type,
                        'salary': getJobDetail.salary.base_salary,
                        'Jobtype_Salary': getJobDetail.salary.id,
                        'basebay': getJobDetail.base_pay,
                        'fix_allow': getJobDetail.salary.fixed_allow,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    },
                )

            if action == "getAllData":
                if request.user.has_perm('Hr.view_jobdetails'): 
                    id = request.POST.get('id')
                    depart_id = request.POST.get('depart_id')
                    getjobDetail = JobDetails.objects.filter(
                        employee=id)
                    message = []
                    for xjobdetail in range(0, len(getjobDetail)):
                        # get_department = Departments.objects.get(id = getjobDetail[xjobdetail].department_all.id)
                        # get_depart_section_id = Depart_Sections.objects.get(id = get_department.id)



                        message.append({
                            # 'id': getjobDetail[xjobdetail].id,
                            # 'job_type': getjobDetail[xjobdetail].job_type.name,
                            # 'employee_type': getjobDetail[xjobdetail].employee_type,
                            # 'department_name': getjobDetail[xjobdetail].department_all.department_name,
                            
                            # 'section_department': 'No section ' if  getjobDetail[xjobdetail].depar_section == None  else   getjobDetail[xjobdetail].depar_section.department_sections,
                            # 'base_salary': getjobDetail[xjobdetail].salary.base_salary,
                            # 'fixed_allow': getjobDetail[xjobdetail].salary.fixed_allow,
                            # 'base_pay': getjobDetail[xjobdetail].base_pay,
                            # 'status': "Active " if getjobDetail[xjobdetail].is_active is True else "Inactive",

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'Access is Denied! ',
                        'title': 'No Access Permission',
                        'type': 'warning',

                    },
                )
            if action == "get_deb_section_func":
              
                    id = request.POST.get('id')
                    depart_id = request.POST.get('department')

                    get_depart_id = Depart_Sections.objects.filter(
                        departments=depart_id)

                    message = []
                    for xjobdetail in range(0, len(get_depart_id)):

                        message.append({
                            'id': get_depart_id[xjobdetail].id,
                            'name': get_depart_id[xjobdetail].department_sections,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
        
            if action == "get_salary_func":
              
                    id = request.POST.get('id')
                    depart_id = request.POST.get('department')

                    get_depart_id = Salary.objects.filter(
                        job_type=depart_id)

                    message = []
                    for xjobdetail in range(0, len(get_depart_id)):

                        message.append({
                            'id': get_depart_id[xjobdetail].id,
                            'base_salary': get_depart_id[xjobdetail].base_salary,
                            'name': get_depart_id[xjobdetail].name,
                        
                        
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

            if action == "get_sub_category_salary_func":
              
                    id = request.POST.get('id')
                    subsalary = request.POST.get('subsalary')

                    sbsalary = Salary.objects.filter(
                        id=subsalary)

                    message = []
                    for xsubsalary in range(0, len(sbsalary)):

                        message.append({
                            'id': sbsalary[xsubsalary].id,
                            'base_salary': sbsalary[xsubsalary].base_salary,
                            'name': sbsalary[xsubsalary].name,
                        
                        
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

            if action == "get_director_assistance_func":
              
                    id = request.POST.get('id')
                    secretary = request.POST.get('secretary')

                    getDirectorAssistance = Secretary.objects.filter(
                            director = secretary  )

                    message = []
                    for xdirAssis in range(0, len(getDirectorAssistance)):

                        message.append({
                            'id': getDirectorAssistance[xdirAssis].id,
                            'name': getDirectorAssistance[xdirAssis].name,
                            
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
        
            if action == "get_departments_func":
              
                    id = request.POST.get('id')
                    departID = request.POST.get('department_id')

                    getDirectorAssistance = Departments.objects.filter(
                            director = departID  )

                    message = []
                    for xdirAssis in range(0, len(getDirectorAssistance)):

                        message.append({
                            'id': getDirectorAssistance[xdirAssis].id,
                            'name': getDirectorAssistance[xdirAssis].department_name,
                            
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
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)

##################################### Banks ################################
@login_required(login_url='Login')

def manage_EmployeeAccount(request, action):
    try:
        if request.method == "POST":
            if action == 'new_Employe_Bank':

                if request.user.has_perm('Hr.add_employeebank'):
                    # Get all data from the request
                    employee_id = request.POST.get('employee_id')
                    banks = request.POST.get('banks')
                    Account = request.POST.get('Account')
                    print('436t4544')
                    # Validaet data

                    if banks == '' or banks == 'null' or banks is None or banks == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'what is your Banks ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Account == '' or Account == 'null' or Account is None or Account == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter work location',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if number_validation(Account) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter number only for  bank account',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    # getting employee instance
                    get_employee = Employee.objects.get(id=employee_id)
                    allBanks = Banks.objects.get(id=banks)
                    employee_Banks = EmployeeBank(employee=get_employee, banks=allBanks, account_number=Account)
                    employee_Banks.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Bank has been created',
                            'title': 'successfully created !',
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

                    },
                )
            if action == 'update_Bank':
                if request.user.has_perm('Hr.change_employeebank'):
                    employee_id = request.POST.get('employee_id')
                    banks = request.POST.get('banks')
                    Account = request.POST.get('Account')

                    id = request.POST.get('id')

                    # Validaet data
                    if banks == '' or banks == 'null' or banks is None or banks == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'what is your Banks ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if Account == '' or Account == 'null' or Account is None or Account == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter work location',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if number_validation(Account) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter number only for  bank account',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    update_bank_detail = EmployeeBank.objects.get(id=id)
                    get_Bank = Banks.objects.get(id=banks)

                    update_bank_detail.banks = get_Bank
                    update_bank_detail.account_number = Account

                    update_bank_detail.save()
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'{get_Bank.name} has been updated',
                            'title': "re bank up[dated]",
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

                    },
                )
            if action == "getBankData":
             
                    id = request.POST.get('id')
                    getBankDetail = EmployeeBank.objects.get(
                        id=id)

                    message = {
                        'id': getBankDetail.id,
                        'bank': getBankDetail.banks.id,
                        'Account': getBankDetail.account_number,

                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
            if action == "getAllBankData":
                if request.user.has_perm('Hr.view_employeebank'):
                    id = request.POST.get('id')
                    if EmployeeBank.objects.filter(employee=id).exists():
                        getemployeBankDetail = EmployeeBank.objects.filter(employee=id)
                        message = []
                        for xjobdetail in range(0, len(getemployeBankDetail)):
                                message.append({
                                    'id': getemployeBankDetail[xjobdetail].id,
                                    'banks': getemployeBankDetail[xjobdetail].banks.name,
                                    'EmployeeName': getemployeBankDetail[xjobdetail].employee.get_full_name(),
                                    'account_number': getemployeBankDetail[xjobdetail].account_number,
                                    # 'work_shift': getemployeBankDetail[xjobdetail].work_shift,
                                    # 'status': "Active " if getemployeBankDetail[xjobdetail].is_active is True else "InActive",

                                })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)
                    else:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Bank Does not axisted',
                                'title': 'successfully found !',
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

                        },
                    )
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

def view_PendingJobs_Employe(request):
    try:
        if request.user.has_perm('Hr.Approve_employee '):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 30
            SearchQuery = ''
            EmployeeList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                EmployeeList = JobDetails.objects.filter(
                    Q(job_type__name__icontains=SearchQuery) |
                    Q(employee__first_name__icontains=SearchQuery) |
                    Q(employee__father_name__contains=SearchQuery) |                
                    Q(employee__last_name__contains=SearchQuery) |                
                    Q(employee__empl_number__icontains=SearchQuery),
                    is_active = False



                )
            else:
                EmployeeList = JobDetails.objects.filter(is_active = False, employee__is_terminated = False,job_state = 'Pending')

            paginator = Paginator(EmployeeList, DataNumber,)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_obj': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Employee List',
                'job_type_all': JobType.objects.all(),
                'diractrates': Directorate.objects.all(),
                'secretory_id': Secretary.objects.all(),
                

            





            }
            return render(request, 'Hr/Pending_jobs.html', context)

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
def manage_PendingJobs_employee(request, activity):
    try:
        if request.method == "POST":                
            if activity == 'approve_reject_jobs':
                if request.user.has_perm('Hr.Approve_employee'):
                    employee_id = request.POST.get('employee_id')
                    jobDetID = request.POST.get('jobDetID')
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

                    if jobDetID == '' or jobDetID == 'null' or jobDetID is None or jobDetID == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'No Job Detail ID',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )   
                        
                    if employee_id == '' or employee_id == 'null' or employee_id is None or employee_id == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'No Employee ID',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
            
                    if status == 'Approved':
                        if request.user.has_perm('Hr.Approve_employee'):  
                            deactivateLastJob=  JobDetails.objects.filter(employee_id = employee_id, is_active = True)
                            if len(deactivateLastJob)>0:
                                deactivateLastJob[0].is_active = False
                                deactivateLastJob[0].job_state = 'inactive'                          
                                deactivateLastJob[0].save()

                            job_details_current = JobDetails.objects.get(id=jobDetID)              
                            job_details_current.is_active = True
                            job_details_current.appprovedwho = request.user.username
                            job_details_current.job_state = "Approved"
                            job_details_current.save()
                        else:
                            return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Access is Denied! ',
                                        'title': 'No Access Permission',
                                        'type': 'warning',

                                    },
                                    )
                    if status == 'Rejected':                            
                        job_details_current = JobDetails.objects.get(id=jobDetID)                  
                        job_details_current.is_active = False
                        job_details_current.job_state = "Rejected"
                        job_details_current.save()

                    if status == 'Pending':
                        job_details_current = JobDetails.objects.get(id=jobDetID)                  
                        job_details_current.is_active = False
                        job_details_current.job_state = "Pending"
                        job_details_current.save()  
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
                            'Message': 'Access is Denied! ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                        )
            if activity == "get_job_detail_all":  
                if request.user.has_perm('Hr.view_jobdetails'):
                    id = request.POST.get('id')              
                    getjobDetail = JobDetails.objects.filter(
                        id=id)
                    message = []
                    for xjobdetail in range(0, len(getjobDetail)):
                       
                        message.append({
                            'id': getjobDetail[xjobdetail].id,                            
                            'job_type': getjobDetail[xjobdetail].job_type.id,
                            'employee_type': getjobDetail[xjobdetail].employee_type,
                            'department_name':'no' if  getjobDetail[xjobdetail].department_all is None else getjobDetail[xjobdetail].department_all.id ,                        
                            'section_department':'no' if getjobDetail[xjobdetail].depar_section is None else getjobDetail[xjobdetail].depar_section.id,
                            'Director': getjobDetail[xjobdetail].director.id,
                            'secretary':'no' if getjobDetail[xjobdetail].secretory is None else getjobDetail[xjobdetail].secretory.id,
                            'jobytpesalary': getjobDetail[xjobdetail].salary.id,
                            'base_salary': getjobDetail[xjobdetail].salary.base_salary,
                            'fixed_allow': getjobDetail[xjobdetail].salary.fixed_allow,
                            'base_pay': getjobDetail[xjobdetail].base_pay,
                            'status': "Active " if getjobDetail[xjobdetail].is_active is True else "Inactive",

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
            'Message': 'On Error Occurs . Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)



def printDetail(request,id):
    try:
        id = id
        alljob = JobDetails.objects.get(id  = id)
        emplID = alljob.employee.id   

        qualification = ''
        if Qualification.objects.filter(employee_id= emplID).exists():
           qualification = Qualification.objects.filter(employee_id= emplID)


        experience = ''
        if Experience.objects.filter(employee_id = emplID).exists():
           experience = Experience.objects.filter(employee_id= emplID)
        
        print(qualification, 'waa kan ')


        
        context = {
            'isError': False,
            'id':id,
            'alljob':alljob,
            'qualification':   qualification ,          
            'experience':experience,          
            }
        return render(request,'Hr/printEml.html',context)
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