from django.shortcuts import render
from django.urls import reverse_lazy
from Hr.models import Employee
from Hr.views import text_validation, text_validationNumber
from Users.models import sendException
from .models import *
from Inventory.models import Medicine ,Medicine_categories, Equipment, Equipment_categories , MedicineTransection
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Users.models import Users
currentDate = date.today()
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When


# remove special character
def RemoveSpecialCharacters(text):
    # A list of special characters
    if text == '':
        return ''
    else:

        special_characters = ["+", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", "/", "=", "==", "<", ">", "$", "#", "/", ";", "_", "%",
                              "~", "*", "?", ":", "\"", "\\"]
        # using lambda function to find if the special characters are in the list
        # Converting list to string using the join method
        normal_string = "".join(
            filter(lambda char: char not in special_characters, text))
        return normal_string

@login_required(login_url='Login')
def radiology_exam_orders(request):
    try:
        if request.user.has_perm('LRPD.view_radiologyorders'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            radiologyResult = []
            Status ="Pending"
            Collected_by = Employee.objects.all()
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                radiologyResult = RadiologyOrders.objects.filter(
                    Q(Status__icontains=Status)
                                             &  (
                    Q(Appointment__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Appointment__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Appointment__Patient__PatientLastName__icontains=SearchQuery) |
                    Q(Appointment__Doctor__first_name__icontains=SearchQuery)|
                    Q(Appointment__Doctor__father_name__icontains=SearchQuery)|
                    Q(Appointment__Doctor__last_name__icontains=SearchQuery)|
                    
                    Q(Admission__Admission_order__Appointment__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Patient__PatientLastName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Appointment__Doctor__father_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Appointment__Doctor__last_name__icontains=SearchQuery)|
                    
                    Q(Admission__Admission_order__Visit__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Visit__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Visit__Patient__PatientLastName__icontains=SearchQuery) |
                    
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|

                    Q(Visit__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Visit__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Visit__Patient__PatientLastName__icontains=SearchQuery) |
                   Q(Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                   Q(Visit__emergencytriage__Doctor__father_name__icontains=SearchQuery)|
                   Q(Visit__emergencytriage__Doctor__last_name__icontains=SearchQuery)|
                   
                    Q(RadiologyOrderNumber__icontains=SearchQuery)|
                    Q(Ordered_by__icontains=SearchQuery))
                )
            else:
                radiologyResult = RadiologyOrders.objects.filter(Status=Status).order_by(
                        Case(
                            When(Ordered_by="Emergency Department", then=1),
                            When(Ordered_by="Inpatient Unit", then=2),
                            When(Ordered_by="Outpatient Unit", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )

            paginator = Paginator(radiologyResult, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Radiology Result List',
                'collected_by': Collected_by,
            }
            return render(request, 'radiology/radiology-exam-orders.html', context)
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
def radiology_result(request):
    try:
        if request.user.has_perm('LRPD.view_radiologyorders'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            radiologyResult = []
            Status ="Approved"
            Collected_by = Employee.objects.all()
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                radiologyResult = RadiologyOrders.objects.filter(
                    Q(Status__icontains=Status)
                                             &  (
                    Q(Appointment__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Appointment__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Appointment__Patient__PatientLastName__icontains=SearchQuery) |
                    Q(Appointment__Doctor__first_name__icontains=SearchQuery)|
                    Q(Appointment__Doctor__father_name__icontains=SearchQuery)|
                    Q(Appointment__Doctor__last_name__icontains=SearchQuery)|
                    
                    Q(Admission__Admission_order__Appointment__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Patient__PatientLastName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Appointment__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Appointment__Doctor__father_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Appointment__Doctor__last_name__icontains=SearchQuery)|
                    
                    Q(Admission__Admission_order__Visit__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Visit__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Admission__Admission_order__Visit__Patient__PatientLastName__icontains=SearchQuery) |
                    
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                    Q(Admission__Admission_order__Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|

                    Q(Visit__Patient__PatientFirstName__icontains=SearchQuery) |
                    Q(Visit__Patient__PatientMiddleName__icontains=SearchQuery) |
                    Q(Visit__Patient__PatientLastName__icontains=SearchQuery) |
                   Q(Visit__emergencytriage__Doctor__first_name__icontains=SearchQuery)|
                   Q(Visit__emergencytriage__Doctor__father_name__icontains=SearchQuery)|
                   Q(Visit__emergencytriage__Doctor__last_name__icontains=SearchQuery)|
                   
                    Q(RadiologyOrderNumber__icontains=SearchQuery)|
                    Q(Ordered_by__icontains=SearchQuery))
                )
            else:
                radiologyResult = RadiologyOrders.objects.filter(Status=Status).order_by(
                        Case(
                            When(Ordered_by="Emergency Department", then=1),
                            When(Ordered_by="Inpatient Unit", then=2),
                            When(Ordered_by="Outpatient Unit", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )
            paginator = Paginator(radiologyResult, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Radiology Result List',
                'collected_by': Collected_by,
            }
            return render(request, 'radiology/radiology-result.html', context)
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
def manage_radiologyresult(request, action):
    # try:
        if request.method == 'POST':
            if action == 'new_radiologyresult':
                if request.user.has_perm('LRPD.add_radiologyresult'):
                    # Get all data from the request
                    Collected_by = request.POST.get('Collected_by')
                    order_id = request.POST.get('ID')
                    CollectionDate = request.POST.get('CollectionDate')
                    
                    findings = request.POST.get('findings')
                    impressions = request.POST.get('impressions')
                    recommendations = request.POST.get('recommendations')
                    comments = request.POST.get('comments')
                    
                    examID = request.POST.get('examID')
                    # result_files = request.POST.get('result_files')
                    files = []
                        
                    if examID:
                        examID = [x for x in examID.split(',')]
                        
                
                    if Collected_by == '' or Collected_by == 'null' or Collected_by is None or Collected_by == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose who collected this Test',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        ) 
                    if CollectionDate == '' or CollectionDate == 'null' or CollectionDate is None or CollectionDate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose when collected this Test',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        ) 

                    if len(examID) != 0:     
                        findings = [x for x in findings.split(':')]
                        for value in range(0, len(findings )):
                            if findings[value] == '' or findings[value]== 'null' or findings[value] is None or findings[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter findings',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(findings[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for findings',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            findings[value] = RemoveSpecialCharacters(findings[value])
                            
                        impressions = [x for x in impressions.split(':')]
                        for value in range(0, len(impressions )):
                            if impressions[value] == '' or impressions[value]== 'null' or impressions[value] is None or impressions[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter impressions',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(impressions[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for impressions',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            impressions[value] = RemoveSpecialCharacters(impressions[value])

                        recommendations = [x for x in recommendations.split(':')]
                        for value in range(0, len(recommendations )):
                            if recommendations[value] == '' or recommendations[value]== 'null' or recommendations[value] is None or recommendations[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Recommendations',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(recommendations[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for recommendations',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            recommendations[value] = RemoveSpecialCharacters(recommendations[value])

                        comments = [x for x in comments.split(':')]
                        for value in range(0, len(comments )):
                            if comments[value] == '' or comments[value]== 'null' or comments[value] is None or comments[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Comment',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(comments[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for comments',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            comments[value] = RemoveSpecialCharacters(comments[value])

                        for id in examID:
                            try:
                                print('result_files_'+str(id))
                                
                                file = request.FILES['result_files_'+str(id)]
                                print(file, 'nisde')
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
                            files.append(file)
                            

                        print(files, 'fil above')
                
                    get_radio_order_id = RadiologyOrders.objects.get(id=order_id)
                    get_radio_order_id.Status = "Approved"
                    get_radio_order_id.save()      
                    collected_emp = Employee.objects.get(id=Collected_by)
                    # data_entered_by = Users.objects.get(id=request.user.id)
                    print(files, 'fil')
                    RadioResults = RadiologyResult( RadiologyOrder_id=get_radio_order_id.id, Collected_by_id= collected_emp.id, CollectionDate=CollectionDate)
                    RadioResults.save()
                    radio_result = RadiologyResult.objects.get(id=RadioResults.id)
                    for (finding, impression, recommendation, comment, examid,fil) in zip(findings, impressions, recommendations, comments, examID, files):
                        print(fil, 'filbelow')
                        # blood result
                        # print(test_no, 'testnumber waa')
                        radio_exam = RadiologyExam.objects.get(id=examid)
                        radiologyResultDetail = RadiologyResultDetails(Radiology_Result_id=radio_result.id, RadiologyExam_id=radio_exam.id, Findings=finding, Impressions=impression, Recommendations = recommendation, Comments = comment, Result_Files=fil)
                        radiologyResultDetail.save()
                
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Radiology Result has been created',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission add radiology result',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
                
            if action == 'edit_radiologyresult':
                if request.user.has_perm('LRPD.add_radiologyresult'):
                    # Get all data from the request
                    Collected_by = request.POST.get('Collected_by')
                    order_id = request.POST.get('ID')
                    CollectionDate = request.POST.get('CollectionDate')
                    
                    findings = request.POST.get('findings')
                    impressions = request.POST.get('impressions')
                    recommendations = request.POST.get('recommendations')
                    comments = request.POST.get('comments')
                    
                    examID = request.POST.get('examID')
                    # result_files = request.POST.get('result_files')
                
                        
                    if examID:
                        examID = [x for x in examID.split(',')]
                        
                
                    if Collected_by == '' or Collected_by == 'null' or Collected_by is None or Collected_by == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose who collected this Test',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        ) 
                    if CollectionDate == '' or CollectionDate == 'null' or CollectionDate is None or CollectionDate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Choose when collected this Test',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        ) 

                    if len(examID) != 0:     
                        findings = [x for x in findings.split(':')]
                        for value in range(0, len(findings )):
                            if findings[value] == '' or findings[value]== 'null' or findings[value] is None or findings[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter findings',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(findings[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for findings',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            findings[value] = RemoveSpecialCharacters(findings[value])
                            
                        impressions = [x for x in impressions.split(':')]
                        for value in range(0, len(impressions )):
                            if impressions[value] == '' or impressions[value]== 'null' or impressions[value] is None or impressions[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter impressions',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(impressions[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for impressions',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            impressions[value] = RemoveSpecialCharacters(impressions[value])

                        recommendations = [x for x in recommendations.split(':')]
                        for value in range(0, len(recommendations )):
                            if recommendations[value] == '' or recommendations[value]== 'null' or recommendations[value] is None or recommendations[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Recommendations',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(recommendations[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for recommendations',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            recommendations[value] = RemoveSpecialCharacters(recommendations[value])

                        comments = [x for x in comments.split(':')]
                        for value in range(0, len(comments )):
                            if comments[value] == '' or comments[value]== 'null' or comments[value] is None or comments[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Comment',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if text_validationNumber(comments[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for comments',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                            comments[value] = RemoveSpecialCharacters(comments[value])

                    
                        try:
                            
                            file = request.FILES['result_files']
                        except KeyError:
                                file = None
                        # if file is None or file == '':
                        #     message = {
                        #         'isError': True,
                        #         'title': "Validation Error",
                        #         'type': "warning",
                        #         'Message': 'Please upload photo.'
                        #     }
                        #     return JsonResponse(message, status=200)
                        if file:
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

                
                
                    get_radio_order_id = RadiologyOrders.objects.get(id=order_id)
                    # get_radio_order_id.Status = "Approved"
                    # get_radio_order_id.save()      
                    collected_emp = Employee.objects.get(id=Collected_by)
                    # data_entered_by = Users.objects.get(id=request.user.id)
                    update_radio_result = RadiologyResult.objects.get(RadiologyOrder=get_radio_order_id.id)
                    update_radio_result.Collected_by_id = collected_emp.id
                    update_radio_result.CollectionDate = CollectionDate
                    update_radio_result.save()
                    update_radio_result_details = RadiologyResultDetails.objects.filter(Radiology_Result=update_radio_result.id)
                    for update_radio_result_detail in update_radio_result_details:
                        for (finding, impression, recommendation, comment, examid) in zip(findings, impressions, recommendations, comments, examID):
                        
                            update_radio_result_detail.Findings = finding
                            update_radio_result_detail.Impressions = impression
                            update_radio_result_detail.Recommendations = recommendation
                            update_radio_result_detail.Comments = comment
                            if file:
                                update_radio_result_detail.Result_Files = file
                            update_radio_result_detail.save()
                          
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Radiology Result has been created',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission add radiology result',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'get_radiologi_result_info':
                if request.user.has_perm('LRPD.add_radiologyresult'):
                    id = request.POST.get('orderid')
                    
                    radiology_order = RadiologyOrders.objects.get(id = id)
                    radiologyResult = RadiologyResult.objects.get(RadiologyOrder=radiology_order.id)
                    message = {
                        'OrderId': radiology_order.id,
                        'AppointId': radiology_order.Appointment.id,
                        'Doctor': radiology_order.Doctor.get_full_name(),
                        'PatientName': radiology_order.Appointment.Patient.get_fullName(),
                        'PatientAge': radiology_order.Appointment.Patient.PatientAge,
                        'PatientGender': radiology_order.Appointment.Patient.PatientGender,
                        'PatientMobileNo': radiology_order.Appointment.Patient.PatientMobileNo,
                        'PatientDistrict': radiology_order.Appointment.Patient.PatientDistrict,
                        'PatientVillage': radiology_order.Appointment.Patient.PatientVillage,
                        'ResultDate': radiologyResult.Result_date,
                        'Collected_by': radiologyResult.Collected_by.get_full_name(),
                        'resultDocument': radiologyResult.get_document_detail(),
                        'CollectionDate': radiologyResult.CollectionDate,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
    # except Exception as error:
    #     username = request.user.username
    #     name = request.user.first_name + ' ' + request.user.last_name
    #     sendException(
    #         request, username, name, error)
    #     message = {
    #         'title': 'Server Error!',
    #         'type': 'error',
    #         'isError': True,
    #         'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
    #     }
    #     return JsonResponse(message, status=200)

@login_required(login_url='Login')
def RadiologyExam_list(request):
    try:
        if request.user.has_perm('LRPD.view_radiologyexam'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            RadiologyExamList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                RadiologyExamList = RadiologyExam.objects.filter(
                    Q(ExamName__icontains=SearchQuery) |
                    Q(Category__CategoryName__icontains=SearchQuery)
                )
            else:
                RadiologyExamList = RadiologyExam.objects.all()

            paginator = Paginator(RadiologyExamList, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            examcategory = ExamCategory.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'RadiologyExam List',
                'examcategory': examcategory,
            }
            return render(request, 'radiology/Exam.html', context)
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
def manage_RadiologyExam(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_radiologyExam':
                if request.user.has_perm('LRPD.add_radiologyexam'):
                    # Get all data from the request
                    ExamName = request.POST.get('ExamName')
                    ExamDescription = request.POST.get('ExamDescription')
                    category = request.POST.get('category')
                

                    if ExamName == '' or ExamName == 'null' or ExamName is None or ExamName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(ExamName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for exam name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if category == '' or category == 'null' or category is None or category == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Category',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if ExamDescription == '' or ExamDescription == 'null' or ExamDescription is None or ExamDescription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Unit',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(ExamDescription) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for exam description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    ExamName = RemoveSpecialCharacters(ExamName)
                    ExamDescription = RemoveSpecialCharacters(ExamDescription)

                    get_category = ExamCategory.objects.get(id=category)
                    radiologyExam = RadiologyExam(ExamName = ExamName, ExamNumber = GenerateRadiologyNumber(),Category_id = get_category.id, ExamDescription= ExamDescription)
                    radiologyExam.save()
                    
                                        
                    return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'New Radiology Exam has been created',
                                'title': 'Masha Allah !',
                                'type': 'success+',
                            }
                        )    
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission add radiology Exam',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'edit_radiologyExam':
                if request.user.has_perm('LRPD.change_radiologyexam'):
                    # Get all data from the request
                    id = request.POST.get('ExamID')
                    ExamName = request.POST.get('ExamName')
                    ExamDescription = request.POST.get('ExamDescription')
                    category = request.POST.get('category')

                    if ExamName == '' or ExamName == 'null' or ExamName is None or ExamName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(ExamName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for exam name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if category == '' or category == 'null' or category is None or category == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Category',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if ExamDescription == '' or ExamDescription == 'null' or ExamDescription is None or ExamDescription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Unit',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(ExamDescription) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for exam description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    ExamName = RemoveSpecialCharacters(ExamName)
                    ExamDescription = RemoveSpecialCharacters(ExamDescription)
                    exam_category = ExamCategory.objects.get(id=category)
                    update_radiology = RadiologyExam.objects.get(id=id)
                    update_radiology.ExamName= ExamName
                    update_radiology.Category_id= exam_category.id
                    update_radiology.ExamDescription= ExamDescription
                    
                    update_radiology.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'a Radiology Exam has been updated',
                                'title': 'masha allah !' + ExamName + " been updated" ,
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission edit radiology Exam',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            # get radiology exam info for update
            if action == "get_radiologyExam":
                if request.user.has_perm('LRPD.change_radiologyexam'):
                    id = request.POST.get('ExamID')
                    
                    radiology = RadiologyExam.objects.get(id = id)
                    message = {
                        'id': radiology.id,
                        'ExamName': radiology.ExamName,
                        'ExamDescription': radiology.ExamDescription,
                        'category': radiology.Category.id,
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
def radiology_equipment_order(request):
    try:
        if request.user.has_perm('LRPD.view_radiologyequipmentorder'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            radiology_equipment_order_list = []
            status = "Pending"
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                radiology_equipment_order_list = RadiologyEquipmentOrder.objects.filter(
                    Q(Appointment__Patient__get_fullName__icontains=SearchQuery) |
                    Q(Doctor__get_full_name__icontains=SearchQuery)
                )
            else:
                radiology_equipment_order_list = RadiologyEquipmentOrder.objects.filter(Q(Status__icontains=status))

            paginator = Paginator(radiology_equipment_order_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Item = Equipment.objects.all()
            ItemCategory = Equipment_categories.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Radiology Equipment Order List',
                'Items': Item,
                'ItemCategory': ItemCategory,
            }
            return render(request, 'radiology/radiology-equipment-orders.html', context)
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
def manage_radiology_equipment_order(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_radiology_eq_order':
                if request.user.has_perm('LRPD.add_radiologyequipmentorder'):
                    # Get all data from the request
                    ItemName = request.POST.get('ItemName')
                    Quantity = request.POST.get('Quantity')
                    if ItemName == '' or ItemName == 'null' or ItemName is None or ItemName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if Quantity == '' or Quantity == 'null' or Quantity is None or Quantity == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Unit',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    Status = "Pending"
                    ordered_by = Users.objects.get(id=request.user.id)
                    item_id = Equipment.objects.get(id=ItemName)
                    new_radio_equipment_order = RadiologyEquipmentOrder(Item = item_id, Quantity= Quantity, Status=Status,Ordered_by=ordered_by)
                    new_radio_equipment_order.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'A Lab Equipment has been ordered',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission place radiology eqiupment order',
                            'title': 'Access is Denied !',
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
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)   

@login_required(login_url='Login')
def manage_dropdown(request, action):
    try:
        if action == "get_option":
            if request.method == 'GET':
                if request.user.has_perm('LRPD.view_equipment'):
                    id = request.POST.get('ItemCat')
                    items = Equipment.objects.filter(category=id)
                    item_category = []
                    for index, item in enumerate(items):
                        item_category.append({
                            'id': item.id,
                            'name': item.item_name,
                        })
                    
                    message = {
                        'item_category': item_category,
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
def exam_category_list(request):
    try:
        if request.user.has_perm('LRPD.view_examcategory'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            category_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                category_list =ExamCategory.objects.filter(
                    Q(CategoryName__icontains = SearchQuery) 
                )
            else:
                category_list =ExamCategory.objects.all()

            paginator = Paginator(category_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Radiology category List'


            }
            return render (request, 'radiology/examCategory.html',context)
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
def manage_category_radiology(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_category':
                if request.user.has_perm('LRPD.add_examcategory'):
                    # Get all data from the request
                    CategoryName = request.POST.get('CategoryName')
                    Description = request.POST.get('Description')
                    # Validate data
                    if CategoryName == '' or CategoryName == 'null' or CategoryName is None or CategoryName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter category name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(CategoryName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for category name',
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
                
                    if text_validation(Description) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    CategoryName = RemoveSpecialCharacters(CategoryName)
                    Description = RemoveSpecialCharacters(Description)

                    new_category = ExamCategory(CategoryName = CategoryName, Description= Description)
                    new_category.save()
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'New Category has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission add radiology category',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )   
            if action == 'update_category':
                if request.user.has_perm('LRPD.change_examcategory'):
                    # Get all data from the request
                    categories_id = request.POST.get('CategoryID')
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
                    if text_validation(CategoryName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for category name',
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
                
                    if text_validation(Description) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    CategoryName = RemoveSpecialCharacters(CategoryName)
                    Description = RemoveSpecialCharacters(Description)

                    update_category= ExamCategory.objects.get(id=categories_id)
                    update_category.CategoryName = CategoryName
                    update_category.Description = Description
                    
                    update_category.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'A Radiology Exam Category has been updated',
                                'title': 'masha allah !' + CategoryName + " been updated" ,
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission edit radiology category',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )  
            if action == "get-exam-categories":
                if request.user.has_perm('LRPD.change_examcategory'):
                    id = request.POST.get('category_id')
                
                    category_id = ExamCategory.objects.get(id = id)
                    
            

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
def add_radio_result_form(request, pk):
    try:
        if request.user.has_perm('LRPD.add_radiologyresult'):
            RadioOrders = RadiologyOrders.objects.get(id=pk)
            RadiologyOrderDetail = RadiologyOrderDetails.objects.filter(RadiologyOrder_id=RadioOrders.id)
            radiology_exams_list = [radiology for detail in RadiologyOrderDetail 
                            for radiology in RadiologyExam.objects.filter(id=detail.RadiologyExam.id)]
            unique_categories = {exam.Category for exam in radiology_exams_list}
            Collected_by = Employee.objects.filter(job_type__name__icontains = "Nurse")
            context = {
                'RadioOrders': RadioOrders,
                'radiology_exams_list': radiology_exams_list,
                'unique_categories': unique_categories,
                'collected_by': Collected_by,
            }  
            
            return render(request, 'radiology/add_radio_result.html', context)
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
def edit_radio_result_form(request, pk):
    try:
        if request.user.has_perm('LRPD.change_radiologyresult'):
            RadioResults = RadiologyResult.objects.get(RadiologyOrder=pk)
            RadiologyResultDetail = RadiologyResultDetails.objects.filter(Radiology_Result=RadioResults.id)
            radiology_exams_list = [radiology for detail in RadiologyResultDetail 
                            for radiology in RadiologyExam.objects.filter(id=detail.RadiologyExam.id)]
            unique_categories = {exam.Category for exam in radiology_exams_list}
            Collected_by = Employee.objects.filter(job_type__name__icontains = "Nurse")
            context = {
                'RadioResults': RadioResults,
                'radiology_exams_list': radiology_exams_list,
                'RadiologyResultDetails':RadiologyResultDetail,
                'unique_categories': unique_categories,
                'collected_by': Collected_by,
            }  
            
            return render(request, 'radiology/edit_radio_result.html', context)
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


def GenerateRadiologyNumber():
    last_id = RadiologyExam.objects.filter(~Q(ExamNumber=None)).last()
    serial = 0
    if last_id is not None:
        serial = int(last_id.ExamNumber[2:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"RD{serial}"

def GenerateRadiologyOrderNumber():
    last_id = RadiologyOrders.objects.filter(~Q(RadiologyOrderNumber=None)).last()
    serial = 0
    today = datetime.today().strftime('%d/%m/%y')
    today_without_slashes = today.replace('/', '')
    if last_id is not None:
        serial = int(last_id.RadiologyOrderNumber[9:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"RO{today_without_slashes}{serial}"