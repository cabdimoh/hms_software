import re
from django.shortcuts import render
from Hr.models import Employee
from Users.models import sendException
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Users.models import Users
from django.db.models import Case, When
from Hr.views import RemoveSpecialCharacters, text_validation, text_validationNumber, number_validation
currentDate = date.today()
from django.contrib.auth.decorators import login_required

@login_required(login_url='Login')
def lab_result(request):
    try:
        if request.user.has_perm('LRPD.view_labtestorders'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            labresultList = []
            Collected_by = Employee.objects.all()
            status = "Approved"
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                labresultList = LabTestOrders.objects.filter(
                    Q(Status__icontains=status) & (
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

                    Q(TestOrderNumber__icontains=SearchQuery)|
                    Q(Ordered_by__icontains=SearchQuery))
                )
            else:
                labresultList = LabTestOrders.objects.filter(Q(Status__icontains=status) ).order_by(
                        Case(
                            When(Ordered_by="Emergency Department", then=1),
                            When(Ordered_by="Inpatient Unit", then=2),
                            When(Ordered_by="Outpatient Unit", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        ))
            paginator = Paginator(labresultList, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Lab Result List',
                'collected_by': Collected_by,
            }
            return render(request, 'lab/lab-result.html', context)
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
def lab_test_orders(request):
    try:
        if request.user.has_perm('LRPD.view_labtestorders'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            lab_order_List = []
            
            Collected_by = Employee.objects.filter(job_type__name__icontains = "Nurse")
            status = "Pending"
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                lab_order_List = LabTestOrders.objects.filter(
                    Q(Status__icontains=status) & (
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

                    Q(TestOrderNumber__icontains=SearchQuery)|
                    Q(Ordered_by__icontains=SearchQuery))
                )
            else:
                lab_order_List = LabTestOrders.objects.filter(Q(Status__icontains=status) ).order_by(
                        Case(
                            When(Ordered_by="Emergency Department", then=1),
                            When(Ordered_by="Inpatient Unit", then=2),
                            When(Ordered_by="Outpatient Unit", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        ))

            paginator = Paginator(lab_order_List, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Lab Orders List',
                'collected_by': Collected_by,
            }
            return render(request, 'lab/lab-test-orders.html', context)
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
def manage_labresult(request, action):
    try:
        if request.method == 'POST':
            if action == "get_patient_labOrder_info":
                if request.user.has_perm('LRPD.add_labtestresult'):
                    id = request.POST.get('TestID')
                    
                    LabOrders = LabTestOrders.objects.get(id = id)
                    LabTestOrderDetail = LabTestOrderDetails.objects.filter(LabTestOrder_id=LabOrders.id)
                    message = {
                        'OrderId': LabOrders.id,
                        'AppointId': LabOrders.Appointment.id,
                        'Doctor': LabOrders.Doctor.get_full_name(),
                        'PatientName': LabOrders.Appointment.Patient.get_fullName(),
                        'PatientAge': LabOrders.Appointment.Patient.PatientAge,
                        'PatientGender': LabOrders.Appointment.Patient.PatientGender,
                        'PatientMobileNo': LabOrders.Appointment.Patient.PatientMobileNo,
                        'PatientDistrict': LabOrders.Appointment.Patient.PatientDistrict,
                        'PatientVillage': LabOrders.Appointment.Patient.PatientVillage,

                
                
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')    
            if action == "get_labOrder_info":
                if request.user.has_perm('LRPD.add_labtestresult'):
                    id = request.POST.get('TestID')
                    
                    LabOrders = LabTestOrders.objects.get(id = id)
                    LabTestOrderDetail = LabTestOrderDetails.objects.filter(LabTestOrder_id=LabOrders.id)
                    lab_blood =[]
                    groups = LabTestGroups.objects.all()
                    all_groups = {}
                    tests = []
                    for index, item in enumerate(LabTestOrderDetail):
                        if item.Test.Category.CategoryName == "Blood":
                            lab_blood = LabTest_Blood_Properties.objects.filter(TestID=item.Test.id)
                            
                        
                            for  key, value in enumerate(lab_blood):
                                print( value.Group.GroupName)
                                
                                tests.append({
                                    'id': value.TestID.id,
                                    'name': value.TestID.TestName,
                                    'normalRange': value.NormalRange,
                                    'TestUnit': value.TestUnit,
                                    'group': value.Group.GroupName,
                                    'subgroup': value.SubGroup.SubGroupName,
                                    'Category': value.SubGroup.Group.Category.CategoryName,
                                })
                        else:
                            examination_parameter = LabExaminationParameters.objects.filter(Test= item.Test.id)
                            for keyx, valuex in enumerate(examination_parameter):
                                
                                tests.append({
                                    'id': item.Test.id,
                                    'name': item.Test.TestName,
                                    'Category': item.Test.Category.CategoryName,
                                    'type': valuex.Type,
                                    'parameterName': valuex.ParameterName,
                                

                                })
                    message = {
                        'tests': tests,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')    
            if action == 'new_labResult':
                if request.user.has_perm('LRPD.add_labtestresult'):
                    # Get all data from the request
                    order_id = request.POST.get('order_id')
                    
                    
                    CollectionDate = request.POST.get('CollectionDate')
                    Collected_by = request.POST.get('Collected_by')
                    Comment = request.POST.get('Comment')
                    
                    urine_test_id = request.POST.get('urine_test_id')
                    urine_test = request.POST.get('urine_test')
                    stool_test_id = request.POST.get('stool_test_id')
                    stool_test = request.POST.get('stool_test')
                    
                    TestNumber = request.POST.get('TestNumber')
                    ResultValue = request.POST.get('ResultValue')
                    flagvalue = request.POST.get('flagvalue')
                    
                    micro_stool_id = request.POST.get('micro_stool_id')
                    chemical_stool_id = request.POST.get('chemical_stool_id')
                    physical_stool_id = request.POST.get('physical_stool_id')
                    micro_stool = request.POST.get('micro_stool')
                    chemical_stool = request.POST.get('chemical_stool')
                    physical_stool = request.POST.get('physical_stool')
                    
                    micro_urine_id = request.POST.get('micro_urine_id')
                    chemical_urine_id = request.POST.get('chemical_urine_id')
                    physical_urine_id = request.POST.get('physical_urine_id')
                    micro_urine = request.POST.get('micro_urine')
                    chemical_urine = request.POST.get('chemical_urine')
                    physical_urine = request.POST.get('physical_urine')
                    if urine_test_id:
                        urine_test_id = [x for x in urine_test_id.split(',')]
                    if stool_test_id:
                        stool_test_id = [x for x in stool_test_id.split(',')]
                    if TestNumber:
                        TestNumber = [x for x in TestNumber.split(',')]
                    if micro_stool_id:
                        micro_stool_id = [x for x in micro_stool_id.split(',')]
                    if physical_stool_id:   
                        physical_stool_id = [x for x in physical_stool_id.split(',')]
                    if chemical_stool_id:   
                        chemical_stool_id = [x for x in chemical_stool_id.split(',')]
                    if physical_urine_id:
                        physical_urine_id = [x for x in physical_urine_id.split(',')]
                    if chemical_urine_id:
                        chemical_urine_id = [x for x in chemical_urine_id.split(',')]
                    if micro_urine_id:
                        micro_urine_id = [x for x in micro_urine_id.split(',')]

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
                        
                    if Comment != '' :
                        if text_validationNumber(Comment) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text only for Comment name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(urine_test_id) != 0:     
                        urine_test = [x for x in urine_test.split(',')]
                        for urine_test_len in range(0, len(urine_test )):
                            if urine_test[urine_test_len] == '' or urine_test[urine_test_len]== 'null' or urine_test[urine_test_len] is None or urine_test[urine_test_len] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter urine test value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(urine_test[urine_test_len]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text only for urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(stool_test_id) != 0:     
                        stool_test = [x for x in stool_test.split(',')]
                        for value in range(0, len(stool_test )):
                            if stool_test[value] == '' or stool_test[value]== 'null' or stool_test[value] is None or stool_test[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Stool Test value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(stool_test[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for stool test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                
                    if len(TestNumber) != 0: 
                        if flagvalue:
                            if not all(char == "," for char in flagvalue):
                                flagvalue = [x for x in flagvalue.split(',')]
                                for value in range(0, len(flagvalue )):
                                
                                    if resultValue_validation(flagvalue[value]) == False:
                                        return JsonResponse(
                                            {
                                                'isError': True,
                                                'Message': 'Please enter valid text for blood flag',
                                                'title': 'Validation Error!',
                                                'type': 'warning',
                                            }
                                        )
                            
                        ResultValue = [x for x in ResultValue.split(',')]
                        for value in range(0, len(ResultValue )):
                            if ResultValue[value] == '' or ResultValue[value]== 'null' or ResultValue[value] is None or ResultValue[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter blood result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(ResultValue[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for blood result',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(physical_stool_id) != 0:     
                        physical_stool = [x for x in physical_stool.split(',')]
                        for value in range(0, len(physical_stool )):
                            if physical_stool[value] == '' or physical_stool[value]== 'null' or physical_stool[value] is None or physical_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter physical stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(physical_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for physical stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(chemical_stool_id) != 0:     
                        chemical_stool = [x for x in chemical_stool.split(',')]
                        for value in range(0, len(chemical_stool )):
                            if chemical_stool[value] == '' or chemical_stool[value]== 'null' or chemical_stool[value] is None or chemical_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Chemical stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(chemical_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for chemical stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(micro_stool_id) != 0:     
                        micro_stool = [x for x in micro_stool.split(',')]
                        for value in range(0, len(micro_stool)):
                            if micro_stool[value] == '' or micro_stool[value]== 'null' or micro_stool[value] is None or micro_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Microscopic stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(micro_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for microscopic stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(physical_urine_id) != 0:     
                        physical_urine = [x for x in physical_urine.split(',')]
                        for value in range(0, len(physical_urine )):
                            if physical_urine[value] == '' or physical_urine[value]== 'null' or physical_urine[value] is None or physical_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter physical urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(physical_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for pyhsical urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(chemical_urine_id) != 0:     
                        chemical_urine = [x for x in chemical_urine.split(',')]
                        for value in range(0, len(chemical_urine )):
                            if chemical_urine[value] == '' or chemical_urine[value]== 'null' or chemical_urine[value] is None or chemical_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Chemical urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(chemical_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for chemical urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(micro_urine_id) != 0:     
                        micro_urine = [x for x in micro_urine.split(',')]
                        for value in range(0, len(micro_urine)):
                            if micro_urine[value] == '' or micro_urine[value]== 'null' or micro_urine[value] is None or micro_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Microscopic Urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(micro_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for microscopic urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
            
                    get_lab_order_id = LabTestOrders.objects.get(id=order_id)
                    get_lab_order_id.Status = "Approved"
                    get_lab_order_id.save()      
                    LabTestResults = LabTestResult( LabTestOrder_id=order_id, Collected_by_id= Collected_by, CollectionDate=CollectionDate, Comment = Comment)
                    LabTestResults.save()
                    labtest_result = LabTestResult.objects.get(id=LabTestResults.id)
                    for (value, test_no, flag) in zip(ResultValue, TestNumber, flagvalue):
                        # blood result
                        value = RemoveSpecialCharacters(value)
                        flag = RemoveSpecialCharacters(flag)
                      
                        lab_test = LabTests.objects.get(TestNumber=test_no)
                        lab_blood = LabTest_Blood_Properties.objects.get(TestID=lab_test.id)
                        lab_blood_result = Lab_Blood_Results(labTest_result_id=labtest_result.id, TestID_id=lab_blood.id, ResultValue=value, flag=flag)
                        lab_blood_result.save()
                    # urine result
                    for (value, micro_u_id) in zip( micro_urine, micro_urine_id):
                        # Microscopic urine result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=micro_u_id)
                        lab_parameter_micro_u_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_micro_u_result.save()
                        
                    for (value, chemical_u_id) in zip( chemical_urine, chemical_urine_id):
                        # Chemical Urine Result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=chemical_u_id)
                        lab_parameter_chemical_u_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_chemical_u_result.save()
                        
                    for (value, physical_u_id) in zip( physical_urine, physical_urine_id):
                        value = RemoveSpecialCharacters(value)
                        # physical urine result
                        lab_parameter = LabExaminationParameters.objects.get(id=physical_u_id)
                        lab_parameter_physical_u_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_physical_u_result.save()
                        
                    # stool result
                    for (value, micro_s_id) in zip( micro_stool, micro_stool_id):
                        # Microscopic stool result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=micro_s_id)
                        lab_parameter_micro_s_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_micro_s_result.save()
                    for (value, chemical_s_id) in zip( chemical_stool, chemical_stool_id):
                        # Chemical stool Result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=chemical_s_id)
                        lab_parameter_chemical_s_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_chemical_s_result.save()
                    for (value, physical_s_id) in zip( physical_stool, physical_stool_id):
                        # physical stool result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=physical_s_id)
                        lab_parameter_physical_s_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=lab_parameter.Test.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_physical_s_result.save()
                        
                    # when urine test is not urinalaysis
                    for (value, urine_t_id) in zip( urine_test, urine_test_id):
                        # Chemical stool Result
                        # update -temporary solution - we should give parameter but zero results
                        value = RemoveSpecialCharacters(value)
                        test_id = LabTests.objects.get(id=urine_t_id)
                        lab_parameter = LabExaminationParameters.objects.get(Test=test_id.id)
                        lab_parameter_micro_u_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=test_id.id, ResultValue=value, Parameter_id=lab_parameter.id )
                        lab_parameter_micro_u_result.save()
                        
                    # when stool test are not stool examination just a normal test with no parameter
                    # update -temporary solution - we should give parameter but zero results
                    for (value, stool_t_id) in zip( stool_test, stool_test_id):
                        # physical stool result
                        value = RemoveSpecialCharacters(value)
                        test_id = LabTests.objects.get(id=stool_t_id)
                        lab_parameter = LabExaminationParameters.objects.get(Test=test_id.id)
                        lab_parameter_micro_u_result = Lab_ExaminationParameters_Results(labTest_result_id=labtest_result.id, TestID_id=test_id.id, ResultValue=value, Parameter_id=lab_parameter.id)
                        lab_parameter_micro_u_result.save()
                    
                        
                    
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Lab Result has been created',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )  
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add a laboratory test result',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )

            if action == 'edit_labResult':
                if request.user.has_perm('LRPD.change_labtestresult'):
                    # Get all data from the request
                    order_id = request.POST.get('order_id')
                    
                    
                    CollectionDate = request.POST.get('CollectionDate')
                    Collected_by = request.POST.get('Collected_by')
                    Comment = request.POST.get('Comment')
                    
                    urine_test_id = request.POST.get('urine_test_id')
                    urine_test = request.POST.get('urine_test')
                    stool_test_id = request.POST.get('stool_test_id')
                    stool_test = request.POST.get('stool_test')
                    
                    TestNumber = request.POST.get('TestNumber')
                    ResultValue = request.POST.get('ResultValue')
                    flagvalue = request.POST.get('flagvalue')
                    
                    micro_stool_id = request.POST.get('micro_stool_id')
                    chemical_stool_id = request.POST.get('chemical_stool_id')
                    physical_stool_id = request.POST.get('physical_stool_id')
                    micro_stool = request.POST.get('micro_stool')
                    chemical_stool = request.POST.get('chemical_stool')
                    physical_stool = request.POST.get('physical_stool')
                    
                    micro_urine_id = request.POST.get('micro_urine_id')
                    chemical_urine_id = request.POST.get('chemical_urine_id')
                    physical_urine_id = request.POST.get('physical_urine_id')
                    micro_urine = request.POST.get('micro_urine')
                    chemical_urine = request.POST.get('chemical_urine')
                    physical_urine = request.POST.get('physical_urine')
                    print(flagvalue)
                    if urine_test_id:
                        urine_test_id = [x for x in urine_test_id.split(',')]
                    if stool_test_id:
                        stool_test_id = [x for x in stool_test_id.split(',')]
                    if TestNumber:
                        TestNumber = [x for x in TestNumber.split(',')]
                    if micro_stool_id:
                        micro_stool_id = [x for x in micro_stool_id.split(',')]
                    if physical_stool_id:   
                        physical_stool_id = [x for x in physical_stool_id.split(',')]
                    if chemical_stool_id:   
                        chemical_stool_id = [x for x in chemical_stool_id.split(',')]
                    if physical_urine_id:
                        physical_urine_id = [x for x in physical_urine_id.split(',')]
                    if chemical_urine_id:
                        chemical_urine_id = [x for x in chemical_urine_id.split(',')]
                    if micro_urine_id:
                        micro_urine_id = [x for x in micro_urine_id.split(',')]

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
                        
                    if Comment != '' :
                        if text_validationNumber(Comment) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text only for Comment name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(urine_test_id) != 0:     
                        urine_test = [x for x in urine_test.split(',')]
                        for urine_test_len in range(0, len(urine_test )):
                            if urine_test[urine_test_len] == '' or urine_test[urine_test_len]== 'null' or urine_test[urine_test_len] is None or urine_test[urine_test_len] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter urine test value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(urine_test[urine_test_len]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text only for urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(stool_test_id) != 0:     
                        stool_test = [x for x in stool_test.split(',')]
                        for value in range(0, len(stool_test )):
                            if stool_test[value] == '' or stool_test[value]== 'null' or stool_test[value] is None or stool_test[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Stool Test value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(stool_test[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for stool test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                
                    if len(TestNumber) != 0: 
                        if flagvalue:
                            if not all(char == "," for char in flagvalue):
                                flagvalue = [x for x in flagvalue.split(',')]
                                for value in range(0, len(flagvalue )):
                                
                                    if resultValue_validation(flagvalue[value]) == False:
                                        return JsonResponse(
                                            {
                                                'isError': True,
                                                'Message': 'Please enter valid text for blood flag',
                                                'title': 'Validation Error!',
                                                'type': 'warning',
                                            }
                                        )
                            
                        ResultValue = [x for x in ResultValue.split(',')]
                        for value in range(0, len(ResultValue )):
                            if ResultValue[value] == '' or ResultValue[value]== 'null' or ResultValue[value] is None or ResultValue[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter blood result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(ResultValue[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for blood result',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(physical_stool_id) != 0:     
                        physical_stool = [x for x in physical_stool.split(',')]
                        for value in range(0, len(physical_stool )):
                            if physical_stool[value] == '' or physical_stool[value]== 'null' or physical_stool[value] is None or physical_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter physical stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(physical_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for physical stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(chemical_stool_id) != 0:     
                        chemical_stool = [x for x in chemical_stool.split(',')]
                        for value in range(0, len(chemical_stool )):
                            if chemical_stool[value] == '' or chemical_stool[value]== 'null' or chemical_stool[value] is None or chemical_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Chemical stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(chemical_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for chemical stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(micro_stool_id) != 0:     
                        micro_stool = [x for x in micro_stool.split(',')]
                        for value in range(0, len(micro_stool)):
                            if micro_stool[value] == '' or micro_stool[value]== 'null' or micro_stool[value] is None or micro_stool[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Microscopic stool result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        if resultValue_validation(micro_stool[value]) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for microscopic stool test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if len(physical_urine_id) != 0:     
                        physical_urine = [x for x in physical_urine.split(',')]
                        for value in range(0, len(physical_urine )):
                            if physical_urine[value] == '' or physical_urine[value]== 'null' or physical_urine[value] is None or physical_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter physical urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(physical_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for pyhsical urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(chemical_urine_id) != 0:     
                        chemical_urine = [x for x in chemical_urine.split(',')]
                        for value in range(0, len(chemical_urine )):
                            if chemical_urine[value] == '' or chemical_urine[value]== 'null' or chemical_urine[value] is None or chemical_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Chemical urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(chemical_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for chemical urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    if len(micro_urine_id) != 0:     
                        micro_urine = [x for x in micro_urine.split(',')]
                        for value in range(0, len(micro_urine)):
                            if micro_urine[value] == '' or micro_urine[value]== 'null' or micro_urine[value] is None or micro_urine[value] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Microscopic Urine result value',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                            if resultValue_validation(micro_urine[value]) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for microscopic urine test',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
            
                    get_lab_order_id = LabTestOrders.objects.get(id=order_id)
                    get_lab_order_id.Status = "Approved"
                    get_lab_order_id.save()     
                    collected_by = Employee.objects.get(id=Collected_by) 
                    update_labtestresult = LabTestResult.objects.get(LabTestOrder=order_id)
                    update_labtestresult.Collected_by_id = collected_by.id
                    update_labtestresult.CollectionDate = CollectionDate
                    update_labtestresult.Comment = Comment
                    update_labtestresult.save()
                    labtest_result = LabTestResult.objects.get(id=update_labtestresult.id)
                    for (value, test_no, flag) in zip(ResultValue, TestNumber, flagvalue):
                        # blood result
                        value = RemoveSpecialCharacters(value)
                        flag = RemoveSpecialCharacters(flag)
                      
                        lab_test = LabTests.objects.get(TestNumber=test_no)
                        lab_blood = LabTest_Blood_Properties.objects.get(TestID=lab_test.id)
                        update_lab_blood_result = Lab_Blood_Results.objects.get(labTest_result=labtest_result.id)
                        update_lab_blood_result.ResultValue = value
                        update_lab_blood_result.flag = flag
                        update_lab_blood_result.save()
                    # urine result
                    for (value, micro_u_id) in zip( micro_urine, micro_urine_id):
                        # Microscopic urine result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=micro_u_id)
                        update_lab_parameter_micro_u_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        update_lab_parameter_micro_u_result.ResultValue = value
                        update_lab_parameter_micro_u_result.Parameter = lab_parameter.id
                        update_lab_parameter_micro_u_result.save()
                      
                        
                    for (value, chemical_u_id) in zip( chemical_urine, chemical_urine_id):
                        # Chemical Urine Result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=chemical_u_id)
                        lab_parameter_chemical_u_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_chemical_u_result.ResultValue = value
                        lab_parameter_chemical_u_result.save()
                      
                        
                    for (value, physical_u_id) in zip( physical_urine, physical_urine_id):
                        value = RemoveSpecialCharacters(value)
                        # physical urine result
                        lab_parameter_physical_u_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_physical_u_result.ResultValue = value
                        lab_parameter_physical_u_result.save()
                       
                        
                    # stool result
                    for (value, micro_s_id) in zip( micro_stool, micro_stool_id):
                        # Microscopic stool result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=micro_s_id)
                        lab_parameter_micro_s_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_micro_s_result.ResultValue = value
                        lab_parameter_micro_s_result.save()

                       
                    for (value, chemical_s_id) in zip( chemical_stool, chemical_stool_id):
                        # Chemical stool Result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=chemical_s_id)
                        lab_parameter_chemical_s_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_chemical_s_result.ResultValue = value
                        lab_parameter_chemical_s_result.save()
                        
                    for (value, physical_s_id) in zip( physical_stool, physical_stool_id):
                        # physical stool result
                        value = RemoveSpecialCharacters(value)
                        lab_parameter = LabExaminationParameters.objects.get(id=physical_s_id)
                        
                        lab_parameter_physical_s_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_physical_s_result.ResultValue = value
                        lab_parameter_physical_s_result.save()
                    # when urine test is not urinalaysis
                    for (value, urine_t_id) in zip( urine_test, urine_test_id):
                        # Chemical stool Result
                        # update -temporary solution - we should give parameter but zero results
                        value = RemoveSpecialCharacters(value)
                        test_id = LabTests.objects.get(id=urine_t_id)
                        lab_parameter = LabExaminationParameters.objects.get(Test=test_id.id)
                    
                        lab_parameter_micro_u_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_micro_u_result.ResultValue = value
                        lab_parameter_micro_u_result.save()   
                    # when stool test are not stool examination just a normal test with no parameter
                    # update -temporary solution - we should give parameter but zero results
                    for (value, stool_t_id) in zip( stool_test, stool_test_id):
                        # physical stool result
                        value = RemoveSpecialCharacters(value)
                        test_id = LabTests.objects.get(id=stool_t_id)
                        lab_parameter = LabExaminationParameters.objects.get(Test=test_id.id)
                 
                        lab_parameter_micro_u_result = Lab_ExaminationParameters_Results.objects.get(labTest_result=labtest_result.id)
                        lab_parameter_micro_u_result.ResultValue = value
                        lab_parameter_micro_u_result.save()   
                        
                    
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Lab Result has been updated',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )  
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to edit a laboratory test result',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )


            if action == "get_labResult_info":
                if request.user.has_perm('LRPD.add_labtestresult'):
                    id = request.POST.get('orderid')
                    LabOrders = LabTestOrders.objects.get(id = id)
                    labResult = LabTestResult.objects.get(LabTestOrder_id=LabOrders.id)
                    labBloodresults = Lab_Blood_Results.objects.filter(labTest_result=labResult.id)
                    labParameterresults =Lab_ExaminationParameters_Results.objects.filter(labTest_result=labResult.id)
                    
                    blood_results = []
                    other_results = []
                    for index, result in enumerate(labBloodresults):
                        blood_results.append({
                            'name': result.TestID.TestID.TestName,
                            'group': result.TestID.Group.GroupName,
                            'subgroup': result.TestID.SubGroup.SubGroupName,
                            'normalRange': result.TestID.NormalRange,
                            'TestUnit': result.TestID.TestUnit,
                            'ReportValue': result.ResultValue,
                            'flag': result.flag,
                        })
                    for index, other_result in enumerate(labParameterresults):
                        other_results.append({
                            'name': other_result.TestID.TestName,
                            'Type': other_result.Parameter.Type,
                            'Parameter': other_result.Parameter.ParameterName,
                            'ReportValue': other_result.ResultValue,
                        })
                    message = {
                        'OrderId': LabOrders.id,
                        'LabResultID':labResult.id,
                        'AppointId': LabOrders.Appointment.id,
                        'Doctor': LabOrders.Doctor.get_full_name(),
                        'PatientName': LabOrders.Appointment.Patient.get_fullName(),
                        'PatientAge': LabOrders.Appointment.Patient.PatientAge,
                        'PatientGender': LabOrders.Appointment.Patient.PatientGender,
                        'PatientMobileNo': LabOrders.Appointment.Patient.PatientMobileNo,
                        'PatientDistrict': LabOrders.Appointment.Patient.PatientDistrict,
                        'PatientVillage': LabOrders.Appointment.Patient.PatientVillage,
                        'ResultDate': labResult.Result_date,
                        'Collected_by': labResult.Collected_by.get_full_name(),
                        'CollectionDate': labResult.CollectionDate,
                        'Comment': labResult.Comment,
                        'other_results':other_results,
                        'blood_results':blood_results,
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
def add_lab_result_form(request, pk):
    try:
        if request.user.has_perm('LRPD.view_labtestresult'):
            LabOrder = LabTestOrders.objects.get(id=pk)
            LabTestOrderDetail = LabTestOrderDetails.objects.filter(LabTestOrder_id=LabOrder.id)
            lab_blood_properties = LabTest_Blood_Properties.objects.filter(TestID__in=[detail.Test.id for detail in LabTestOrderDetail])
            unique_groups = LabTestGroups.objects.filter(id__in=[blood.Group.id for blood in lab_blood_properties])
            unique_subgroups = LabTestSubGroups.objects.filter(id__in=[blood.SubGroup.id for blood in lab_blood_properties if blood.SubGroup is not None])
            unique_sample_types = list(set([detail.Test.SampleType for detail in LabTestOrderDetail]))
            lab_examination_parameters = LabExaminationParameters.objects.filter(Test__in=[detail.Test.id for detail in LabTestOrderDetail]).order_by('Type')
            unique_types = lab_examination_parameters.values_list('Type', flat=True).distinct()
            unique_tests = LabTests.objects.filter(id__in=[detail.Test.id for detail in LabTestOrderDetail])
            collected_by = Employee.objects.filter(job_type__name__icontains = "Nurse")

            context = {
                'LabOrders': LabOrder,
                'lab_blood_properties': lab_blood_properties,
                'unique_groups': unique_groups,
                'unique_subgroups': unique_subgroups,
                'unique_categories': unique_sample_types,
                'unique_types': unique_types,
                'unique_tests': unique_tests,
                'lab_examination_parameters': lab_examination_parameters,
                'collected_by': collected_by,
            }
                    
            return render(request, 'lab/addlabresultdesign.html', context)
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
def edit_lab_result_form(request, pk):
    try:
        if request.user.has_perm('LRPD.change_labtestresult'):
            lab_result = LabTestResult.objects.get(LabTestOrder=pk)
            lab_blood_result = Lab_Blood_Results.objects.filter(labTest_result=lab_result.id)
            lab_permission_result = Lab_Blood_Results.objects.filter(labTest_result=lab_result.id)
            LabTestOrderDetail = LabTestOrderDetails.objects.filter(LabTestOrder_id=pk)
            lab_blood_properties = LabTest_Blood_Properties.objects.filter(TestID__in=[detail.Test.id for detail in LabTestOrderDetail])
            lab_group_ids = LabTestGroups.objects.filter(id__in=[blood.Group.id for blood in lab_blood_properties])
            unique_groups = LabTestGroups.objects.filter(id__in=[group.id for group in lab_group_ids])
            lab_subgroup_ids = LabTestSubGroups.objects.filter(id__in=[blood.SubGroup.id for blood in lab_blood_properties if blood.SubGroup is not None])
            unique_subgroups = LabTestSubGroups.objects.filter(id__in=[subgroup.id for subgroup in lab_subgroup_ids])
            unique_sample_types = list(set([detail.Test.SampleType for detail in LabTestOrderDetail]))
            lab_examination_parameters = LabExaminationParameters.objects.filter(Test__in=[detail.Test.id for detail in LabTestOrderDetail]).order_by('Type')
            unique_types = lab_examination_parameters.values_list('Type', flat=True).distinct()
            unique_tests = LabTests.objects.filter(id__in=[detail.Test.id for detail in LabTestOrderDetail])
            collected_by = Employee.objects.filter(job_type__name__icontains = "Nurse")
            for l in lab_blood_result:
                print(l.id)
            context = {
                'lab_result': lab_result,
                'lab_blood_result': lab_blood_result,
                'lab_permission_result': lab_permission_result,
                'lab_blood_properties': lab_blood_properties,
                'unique_groups': unique_groups,
                'unique_subgroups': unique_subgroups,
                'unique_categories': unique_sample_types,
                'unique_types': unique_types,
                'unique_tests': unique_tests,
                'lab_examination_parameters': lab_examination_parameters,
                'collected_by': collected_by,
            }  
            
            return render(request, 'lab/edit_lab_result.html', context)
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
def GenerateTestOrderNumber():
    last_id = LabTestOrders.objects.filter(~Q(TestOrderNumber=None)).last()
    serial = 0
    today = datetime.today().strftime('%d/%m/%y')
    today_without_slashes = today.replace('/', '')
    if last_id is not None:
        serial = int(last_id.TestOrderNumber[8:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"LO{today_without_slashes}{serial}"

validate_result_value = r'^[a-zA-Z0-9][a-zA-Z0-9^]*$'

def resultValue_validation(text):

    if (re.match(validate_result_value, text)):
        return True
    else:
        return False