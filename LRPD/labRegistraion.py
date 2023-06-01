import re
from django.shortcuts import render
from django.urls import reverse_lazy
from Hr.models import Employee
from Users.models import sendException
from Hr.views import RemoveSpecialCharacters, text_validation, text_validationNumber, number_validation
from .models import *
from APEN.models import Appointments
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Users.models import Users
currentDate = date.today()
from django.contrib.auth.decorators import login_required
@login_required(login_url='Login')           
def LabTests_list(request):
    try:
        if request.user.has_perm('LRPD.view_labtests'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            LabTestList = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                LabTestList = LabTests.objects.filter(
                    Q(TestName__icontains=SearchQuery) |
                    Q(SampleType__icontains=SearchQuery) 
                )
            else:
                LabTestList = LabTests.objects.all()

            paginator = Paginator(LabTestList, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            lab_group = LabTestGroups.objects.all()
            lab_subGroup = LabTestSubGroups.objects.all()
            lab_blood = LabTest_Blood_Properties.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'LabTests List',
                'lab_groups': lab_group,
                'lab_subGroups': lab_subGroup,
                'lab_blood':lab_blood,
            }
            return render(request, 'lab/test.html', context)
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
def manage_labtest(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_test':
                if request.user.has_perm('LRPD.add_labtests'):
                    # Get all data from the request
                    TestName = request.POST.get('TestName')
                    TestUnit = request.POST.get('TestUnit')
                    TestDescription = request.POST.get('TestDescription')
                    NormalRange = request.POST.get('NormalRange')
                    Group = request.POST.get('Group')
                    SubGroup = request.POST.get('SubGroup')
                    sampleType = request.POST.get('sampleType')
                    Microscopic = request.POST.get('Microscopic')
                    Physical = request.POST.get('Physical')
                    Chemical = request.POST.get('Chemical')
                    ShortName = request.POST.get('ShortName')
                    ResultType = request.POST.get('ResultType')

                    if TestName == '' or TestName == 'null' or TestName is None or TestName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(TestName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter test name' + TestName + " is not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if ShortName == '' or ShortName == 'null' or ShortName is None or ShortName == 'undefined':
                        return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Short Name',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                    if text_validation(ShortName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter short name' + ShortName + " is not valid short name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if TestDescription == '' or TestDescription == 'null' or TestDescription is None or TestDescription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validationNumber(TestDescription) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Description' + TestDescription + " is not valid Description",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if sampleType == '' or sampleType == 'null' or sampleType is None or sampleType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if ResultType == '' or ResultType == 'null' or ResultType is None or ResultType == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Select Result Type',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if ResultType == "Quantitative":
                        if TestUnit == '' or TestUnit == 'null' or TestUnit is None or TestUnit == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Test Unit',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if unitTest_validation(TestUnit) == False:
                            return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter test unit' + TestUnit + " is not valid test unit",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                             )
                        
                        if Group == '' or Group == 'null' or Group is None or Group == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Test Description',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if SubGroup == '' or SubGroup == 'null' or SubGroup is None or SubGroup == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Test Description',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        
                    
                        if NormalRange == '' or NormalRange == 'null' or NormalRange is None or NormalRange == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Normal Range of The Test',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if number_validation(NormalRange) == False:
                            return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter NormalRange' + NormalRange + " is not valid NormalRange",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                             )
                    elif ResultType == "Multi":
                        if ',' in Microscopic:
                            Microscopic = [x for x in Microscopic.split(',')]
                            for micro in range(0, len(Microscopic)):
                                if Microscopic[micro] == '' or Microscopic[micro]== 'null' or Microscopic[micro] is None or Microscopic[micro] == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter Microscopic Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(Microscopic[micro]) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter Microscopic name, it is not valid Microscopic name",
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                        else:
                            Microscopic = [x for x in Microscopic.split(',')]
                            for micro in Microscopic:
                                if micro == '' or micro== 'null' or micro is None or micro == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter Microscopic Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(micro) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter Microscopic name, it is not valid Microscopic name",
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                         
                        if ',' in Physical:
                            Physical = [x for x in Physical.split(',')]
                            for phys in range(0, len(Physical)):
                                if Physical[phys] == '' or Physical[phys]== 'null' or Physical[phys] is None or Physical[phys] == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter physical Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(Physical[phys]) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter physical name, it is not valid physical name",
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                        else:
                            Physical = [x for x in Physical.split(',')]
                            for phys in Physical:
                                if phys == '' or phys== 'null' or phys is None or phys == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter physical Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(phys) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter physical name, it is not valid physical name",
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                        if ',' in Chemical:
                            Chemical = [x for x in Chemical.split(',')]
                            for chemic in range(0, len(Chemical)):
                                if Chemical[chemic] == '' or Chemical[chemic]== 'null' or Chemical[chemic] is None or Chemical[chemic] == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter Chemical Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(Chemical[chemic]) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter Chemical name, it is not valid Chemical name",                                            
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                        else:
                            Chemical = [x for x in Chemical.split(',')]
                            for chemic in Chemical:
                                if chemic == '' or chemic== 'null' or chemic is None or chemic == 'undefined':
                                    return JsonResponse(
                                        {
                                        'isError': True,
                                        'Message': 'Enter Chemical Examination',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                    )
                                if text_validation(chemic) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': "Please enter Chemical name, it is not valid Chemical name",                                            
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                    TestName = RemoveSpecialCharacters(TestName)
                    ShortName = RemoveSpecialCharacters(ShortName)
                    TestDescription = RemoveSpecialCharacters(TestDescription)
                    NormalRange = RemoveSpecialCharacters_normalrange(NormalRange)
                    TestUnit = RemoveSpecialCharacters_unitTest(TestUnit)
                   

                    if  ResultType == "Quantitative" :
                        LabTest = LabTests(TestName = TestName, ShortName=ShortName, TestNumber = GenerateTestNumber(), TestDescription=TestDescription, SampleType = sampleType)
                        LabTest.save()
                        current_test = LabTests.objects.get(id=LabTest.id)
                        Group_id = LabTestGroups.objects.get(id=Group)
                        subgroup_id = LabTestSubGroups.objects.get(id=SubGroup)
                        blood_properties = LabTest_Blood_Properties(TestID_id= current_test.id, NormalRange=NormalRange, TestUnit= TestUnit, Group_id = Group_id.id, SubGroup_id = subgroup_id.id)
                        blood_properties.save()
                    elif ResultType == "Qualitative" and sampleType == "Blood":
                        LabTest = LabTests(TestName = TestName, ShortName=ShortName, TestNumber = GenerateTestNumber(), TestDescription=TestDescription, SampleType = sampleType)
                        LabTest.save()
                        current_test = LabTests.objects.get(id=LabTest.id)
                        Group_id = LabTestGroups.objects.get(id=Group)
                        if SubGroup:

                            subgroup_id = LabTestSubGroups.objects.get(id=SubGroup)
                            blood_properties = LabTest_Blood_Properties(TestID_id= current_test.id, NormalRange='-', TestUnit= '-', Group_id = Group_id.id, SubGroup_id = subgroup_id.id)
                            blood_properties.save()
                        else:
                            blood_properties = LabTest_Blood_Properties(TestID_id= current_test.id, NormalRange='-', TestUnit= '-', Group_id = Group_id.id)
                            blood_properties.save()
                    elif ResultType == "Qualitative" and (sampleType == "Urine" or sampleType == "Stool" ):
                        LabTest = LabTests(TestName = TestName, ShortName=ShortName, TestNumber = GenerateTestNumber(), TestDescription=TestDescription, SampleType = sampleType)
                        LabTest.save()
                        # temporary solution for lab paramter result(nonetype .....error)
                        
                        current_test = LabTests.objects.get(id=LabTest.id)
                        type_ = "-"
                        parameter_ = "-"
                        examination_parameters = LabExaminationParameters(Test_id = current_test.id, Type=type_, ParameterName = parameter_)
                        examination_parameters.save()
                    
                    elif ResultType == "Multi" :
                        LabTest = LabTests(TestName = TestName, ShortName=ShortName, TestNumber = GenerateTestNumber(), TestDescription=TestDescription, SampleType = sampleType)
                        LabTest.save()
                        current_test = LabTests.objects.get(id=LabTest.id)
                        for physic in Physical:
                            physic = RemoveSpecialCharacters(physic)

                            type = "Physical"
                            examination_parameters = LabExaminationParameters(Test_id = current_test.id, Type=type, ParameterName = physic)
                            examination_parameters.save()
                        for chemica in Chemical:
                            chemica = RemoveSpecialCharacters(chemica)
                            type = "Chemical"
                            examination_parameters = LabExaminationParameters(Test_id = current_test.id, Type=type, ParameterName = chemica)
                            examination_parameters.save()
                        for micros in Microscopic:
                            micros = RemoveSpecialCharacters(micros)
                            type = "Microscopic"
                            examination_parameters = LabExaminationParameters(Test_id = current_test.id, Type=type, ParameterName = micros)
                            examination_parameters.save()
                    else:
                        return render(request, 'Hr/404.html')
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Lab Test has been created',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add a laboratory test',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )

            if action == 'edit_test':
                if request.user.has_perm('LRPD.change_labtests'):
                    # Get all data from the request
                    id = request.POST.get('TestID')
                    TestName = request.POST.get('TestName')
                    TestUnit = request.POST.get('TestUnit')
                    TestDescription = request.POST.get('TestDescription')
                    NormalRange = request.POST.get('NormalRange')

                    if TestName == '' or TestName == 'null' or TestName is None or TestName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if TestUnit == '' or TestUnit == 'null' or TestUnit is None or TestUnit == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Unit',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if TestDescription == '' or TestDescription == 'null' or TestDescription is None or TestDescription == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Test Description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if NormalRange == '' or NormalRange == 'null' or NormalRange is None or NormalRange == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Normal Range of The Test',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    update_test = LabTests.objects.get(id=id)
                    update_test.TestName= TestName
                    update_test.TestUnit= TestUnit
                    update_test.TestDescription= TestDescription
                    update_test.NormalRange= NormalRange
                    update_test.save()
                    return JsonResponse(
                        {
                                'isError': False,
                                'Message': 'Lab Test has been updated',
                                'title': 'masha allah !' + TestName + " been updated" ,
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to update a laboratory test',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
          
            if action == 'get_test_info':
                if request.user.has_perm('LRPD.add_labtests') or request.user.has_perm('LRPD.change_labtests'):
                    id = request.POST.get('testID')
                    test = LabTests.objects.get(id = id)
                    message={}
                    for t_blood in LabTest_Blood_Properties.objects.filter(TestID=test.id):
                        if t_blood.TestID:
                            normalrange = t_blood.NormalRange
                            testUnit = t_blood.TestUnit
                            group = t_blood.Group.GroupName
                            subgroup = t_blood.SubGroup.SubGroupName
                            if t_blood.NormalRange == '-':
                                resultType = 'Qualitative'
                            else:
                                resultType = 'Quantitative'
                            message = {
                                'id': test.TestNumber,
                                'TestName': test.TestName,
                                'ShortName': test.ShortName,
                                'sampleType': test.SampleType,
                                'TestDescription': test.TestDescription,
                                'resultType': resultType,
                                'normalrange': normalrange,
                                'testUnit': testUnit,
                                'group': group,
                                'subgroup': subgroup,
                            }
                    physical_parameters = []
                    chemical_parameters = []
                    microscopic_parameters = []
                    for t_parameter in LabExaminationParameters.objects.filter(Test=test.id):
                        if t_parameter.Type == "Physical":
                            physical_parameters.append(t_parameter.ParameterName)
                        if t_parameter.Type == "Chemical":
                            chemical_parameters.append(t_parameter.ParameterName)
                        if t_parameter.Type == "Microscopic":
                            microscopic_parameters.append(t_parameter.ParameterName)
 
                        if t_parameter.Type == '-':
                            resultType = 'Qualitative'
                        else:
                            resultType = 'MultiComponent'
                        message = {
                            'id': test.TestNumber,
                            'TestName': test.TestName,
                            'ShortName': test.ShortName,
                            'sampleType': test.SampleType,
                            'TestDescription': test.TestDescription,
                            'resultType': resultType,
                            'physical_parameters': physical_parameters,
                            'chemical_parameters': chemical_parameters,
                            'microscopic_parameters': microscopic_parameters,
                        }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_test":
                if request.user.has_perm('LRPD.add_labtests') or request.user.has_perm('LRPD.change_labtests'):

                    id = request.POST.get('TestID')
                    resultType = ''
                    test = LabTests.objects.get(id = id)
                    for t_blood in LabTest_Blood_Properties.objects.filter(TestID=test.id):
                        if t_blood.TestID:
                            normalrange = t_blood.NormalRange
                            testUnit = t_blood.TestUnit
                            if t_blood.NormalRange == '-':
                                resultType = 'Qualitative'
                            else:
                                resultType = 'Quantitative'
                        
                    for t_parameter in LabExaminationParameters.objects.filter(Test=test.id):
                        if t_parameter.Type == '-':
                            resultType = 'Qualitative'
                        else:
                            resultType = 'MultiComponent'
                    print(resultType)
                    message = {
                        'id': test.id,
                        'TestName': test.TestName,
                        'ShortName': test.ShortName,
                        'sampleType': test.SampleType,
                        'TestDescription': test.TestDescription,
                        'resultType': resultType,
                        'normalrange': normalrange,
                        'testUnit': testUnit,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_group_subgroup":
                if request.user.has_perm('LRPD.add_labtests') or request.user.has_perm('LRPD.change_labtests'):
                    group = request.POST.get('Group')
                    get_subgroup = LabTestSubGroups.objects.filter(Group=group)
                    message = []
                    for xsubgroup in range(0, len(get_subgroup)):

                        message.append({
                            'id': get_subgroup[xsubgroup].id,
                            'name': get_subgroup[xsubgroup].SubGroupName,
                        })
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
def view_lab_setup(request):
    try:
        if request.user.has_perm('LRPD.view_labtestgroups'):

            context = {
                    'Groups': LabTestGroups.objects.all(),
                   

                }
            return render(request, "lab/lab_setup.html", context)
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
def manage_lab_setup(request,action):
    try:
        if request.method == 'POST':

            #------------------------Lab Group------------------------------
            if action == "getLabGroup":
                if request.user.has_perm('LRPD.add_labtestgroups') or request.user.has_perm('LRPD.change_labtestgroups'):
                    single_group = LabTestGroups.objects.all()
                    message = []
                    for xgroup in range(0, len(single_group)):
                        message.append({
                            'id': single_group[xgroup].id,
                            'name': single_group[xgroup].GroupName,
                            'sampleType': single_group[xgroup].sampleType,
                            'discription': single_group[xgroup].GroupDescription,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "getSingleLabGroup":
                if request.user.has_perm('LRPD.add_labtestgroups') or request.user.has_perm('LRPD.change_labtestgroups'):
                    id = request.POST.get('id')
                    get_single_group = LabTestGroups.objects.get(
                        id=id)

                    message = {
                        'id': get_single_group.id,
                        'name': get_single_group.GroupName,
                        'sampleType': get_single_group.sampleType,
                        'discription': get_single_group.GroupDescription,


                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == 'new_LabGroup':
                if request.user.has_perm('LRPD.add_labtestgroups'):
                    lab_group_name = request.POST.get('lab_group_name')
                    lab_group_description = request.POST.get('lab_group_description')

                    if lab_group_name == '' or lab_group_name == 'null' or lab_group_name is None or lab_group_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': "Please Enter lab group name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_group_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter lab group name' + lab_group_name + " is not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                   
                    if lab_group_description == '' or lab_group_description == 'null' or lab_group_description is None or lab_group_description == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + lab_group_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_group_description) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text only for lab group description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    lab_group_name = RemoveSpecialCharacters(lab_group_name)
                    lab_group_description = RemoveSpecialCharacters(lab_group_description)
                    sampleType = "Blood"
                    lab_group = LabTestGroups(GroupName=lab_group_name, GroupDescription=lab_group_description, sampleType = sampleType)
                    lab_group.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new Lab Group called {lab_group_name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add a Lab Test Group',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'edit_LabGroup':
                if request.user.has_perm('LRPD.change_labtestgroups'):
                    lab_group_name = request.POST.get('lab_group_name')
                    lab_group_description = request.POST.get('lab_group_description')
                    sampleType = request.POST.get('sampleType')

                    id = request.POST.get('id')
                    if lab_group_name == '' or lab_group_name == 'null' or lab_group_name is None or lab_group_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': "Please Enter lab group name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_group_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter lab group name' + lab_group_name + " is not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                   
                    if lab_group_description == '' or lab_group_description == 'null' or lab_group_description is None or lab_group_description == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + lab_group_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_group_description) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text only for lab group description',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    lab_group_name = RemoveSpecialCharacters(lab_group_name)
                    lab_group_description = RemoveSpecialCharacters(lab_group_description)
                    sampleType = "Blood"
                    update_lab_group = LabTestGroups.objects.get(id=id)
                    update_lab_group.GroupName = lab_group_name
                    update_lab_group.sampleType = sampleType
                    update_lab_group.GroupDescription = lab_group_description
                    update_lab_group.save()
                    return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'Lab Group has been updated',
                                'title': "re bank up[dated]",
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to update a Lab Test Group',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            #------------------------Lab Sub group------------------------------
            if action == "getLabSubGroup":
                if request.user.has_perm('LRPD.add_labtestsubgroups') or request.user.has_perm('LRPD.change_labtestsubgroups'):
                    single_subgroup = LabTestSubGroups.objects.all()
                    message = []
                    for xsubGroup in range(0, len(single_subgroup)):
                        message.append({
                            'id': single_subgroup[xsubGroup].id,
                            'name': single_subgroup[xsubGroup].SubGroupName,
                            'discription': single_subgroup[xsubGroup].SubGroupDescription,
                            'group': single_subgroup[xsubGroup].Group.GroupName,
                            'sampleType': single_subgroup[xsubGroup].Group.sampleType,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "getSingleLabSubGroup":
                    if request.user.has_perm('LRPD.add_labtestsubgroups') or request.user.has_perm('LRPD.change_labtestsubgroups'):
                        id = request.POST.get('id')
                        get_single_subGroup = LabTestSubGroups.objects.get(
                            id=id)

                        message = {
                            'id': get_single_subGroup.id,
                            'group': get_single_subGroup.Group.GroupName,
                            'group_id': get_single_subGroup.Group.id,
                            'name': get_single_subGroup.SubGroupName,
                            'discription': get_single_subGroup.SubGroupDescription,


                        }
                        return JsonResponse({'isError': False, 'Message': message}, status=200)
                    else:
                        return render(request, 'Hr/404.html')
            if action == 'new_LabSubGroup':
                if request.user.has_perm('LRPD.add_labtestsubgroups'):
                    lab_subgroup_name = request.POST.get('lab_subgroup_name')
                    lab_subgroup_descriptions = request.POST.get('lab_subgroup_descriptions')
                    Choosed_Group = request.POST.get('Choosed_Group')

                    if lab_subgroup_name == '' or lab_subgroup_name == 'null' or lab_subgroup_name is None or lab_subgroup_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': "Please enter lab sub group name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_subgroup_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Sub group name ' + lab_subgroup_name + " is not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if lab_subgroup_descriptions == '' or lab_subgroup_descriptions == 'null' or lab_subgroup_descriptions is None or lab_subgroup_descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + lab_subgroup_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_subgroup_descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for  decription',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    lab_subgroup_name = RemoveSpecialCharacters(lab_subgroup_name)
                    lab_subgroup_descriptions = RemoveSpecialCharacters(lab_subgroup_descriptions)
                    xgroup = LabTestGroups.objects.get(id=Choosed_Group)
                    lab_subGroup = LabTestSubGroups(Group_id = xgroup.id, SubGroupName=lab_subgroup_name,
                                        SubGroupDescription=lab_subgroup_descriptions)
                    lab_subGroup.save()

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': f'new Lab Sub Group called {lab_subgroup_name}  has been created',
                            'title': 'masha allah !',
                            'type': 'success',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add a Lab Test Sub Group',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'edit_LabSubGroup':
                if request.user.has_perm('LRPD.change_labtestsubgroups'):
                    lab_subgroup_name = request.POST.get('lab_subgroup_name')
                    lab_subgroup_descriptions = request.POST.get('lab_subgroup_descriptions')
                    Choosed_Group = request.POST.get('Choosed_Group')

                    id = request.POST.get('id')
                    if lab_subgroup_name == '' or lab_subgroup_name == 'null' or lab_subgroup_name is None or lab_subgroup_name == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': "Please enter lab sub group name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_subgroup_name) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter Sub group name ' + lab_subgroup_name + " is not valid name",
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if lab_subgroup_descriptions == '' or lab_subgroup_descriptions == 'null' or lab_subgroup_descriptions is None or lab_subgroup_descriptions == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'provide description for ' + lab_subgroup_name,
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(lab_subgroup_descriptions) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for  decription',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    lab_subgroup_name = RemoveSpecialCharacters(lab_subgroup_name)
                    lab_subgroup_descriptions = RemoveSpecialCharacters(lab_subgroup_descriptions)
                    xgroup = LabTestGroups.objects.get(id=Choosed_Group)
                
                    update_lab_subgroup = LabTestSubGroups.objects.get(id=id)
                    update_lab_subgroup.SubGroupName = lab_subgroup_name
                    update_lab_subgroup.SubGroupDescription = lab_subgroup_descriptions
                    update_lab_subgroup.Group_id = xgroup.id
                    update_lab_subgroup.save()
                    return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'Lab Sub Group has been updated',
                                'title': "re bank up[dated]",
                                'type': 'success',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to update a Lab Test Sub Group',
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

def GenerateTestNumber():
    last_id = LabTests.objects.filter(~Q(TestNumber=None)).last()
    serial = 0
    if last_id is not None:
        serial = int(last_id.TestNumber[5:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"LTEST{serial}"

validate_unitTest_only = '[1-9a-zA-Z^]'

def unitTest_validation(text):

    if (re.match(validate_unitTest_only, text)):
        return True
    else:
        return False
    
def RemoveSpecialCharacters_normalrange(text):
    # A list of special characters
    if text == '':
        return ''
    else:

        special_characters = ["+", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", "/", "=", "==", "<", ">", "$", "#", "/", ";", "_", "%",
                              "~", "*", "?", ":", "\"", "\\", ",", "'", "&"]
        
        normal_string = "".join(
            filter(lambda char: char not in special_characters, text))
        return normal_string
    
def RemoveSpecialCharacters_unitTest(text):
    # A list of special characters
    if text == '':
        return ''
    else:

        special_characters = ["+", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "=", "==", "<", ">", "$", "#", "/", ";", "_", "%",
                              "~", "?", ":", "\"", "\\", ",", "'", "&"]
        
        normal_string = "".join(
            filter(lambda char: char not in special_characters, text))
        return normal_string

