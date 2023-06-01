import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import outpatient
from django.db.models import Case, When
from LRPD.LabResult import GenerateTestOrderNumber
from LRPD.radiology import GenerateRadiologyOrderNumber
from .models import *
from Hr.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Inventory.models import Medicine, Medicine_categories, MedicineTransection
from LRPD.models import *
from Users.models import Users
from django.contrib.auth.decorators import permission_required
from Users.models import sendException
from Users.views import sendTrials
from Hr.views import RemoveSpecialCharacters, text_validation, text_validationNumber,  number_validation, phone_valid, check
from django.db.models import Sum

validate_text_Number_only = '[0-9A-Za-z//,°]'
def vitalsigns_text_numberValidation(textnumber):

    if (re.match(validate_text_Number_only, textnumber)):
        return True
    else:
        return False

@login_required(login_url='Login')          
def emergency_queue_list(request):
    try:
        if request.user.has_perm('APEN.view_emergencyroomvisit'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            emergency_queue_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                emergency_queue_list = EmergencyRoomVisit.objects.filter(
                Q(Status__icontains="in-queue")&
                    Q(Patient__PatientFirstName__icontains=SearchQuery) 
                
                    
                )
            else:
                emergency_queue_list = EmergencyRoomVisit.objects.filter()
                if request.user.is_superuser:
                    emergency_queue_list = EmergencyRoomVisit.objects.filter(
                        Q(Status__icontains="in-queue")
                    ).order_by(
                        Case(
                            When(emergencytriage__TriageCategory="Immediate", then=1),
                            When(emergencytriage__TriageCategory="Emergent", then=2),
                            When(emergencytriage__TriageCategory="Urgent", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )
                else:
                    if "doctor" in request.user.employee.job_type.name.lower():
                        emergency_queue_list = EmergencyRoomVisit.objects.filter(
                        Q(Status__icontains="in-queue") & Q(emergencytriage__Doctor=request.user.employee)
                        ).order_by(
                            Case(
                                When(emergencytriage__TriageCategory="Immediate", then=1),
                                When(emergencytriage__TriageCategory="Emergent", then=2),
                                When(emergencytriage__TriageCategory="Urgent", then=3),
                                default=4,
                                output_field=models.IntegerField(),
                            )
                        )
                    
            paginator = Paginator(emergency_queue_list, DataNumber)

            title_doctor = Title.objects.filter(name__icontains="Doctor")
            doctorList =[]
            for j in title_doctor:
                Doctor = Employee.objects.filter(job_type=j.id)
                for doc in Doctor:
                    doctorList.append(doc)
            
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            districts = ['Dharkenley', 'Deynile', 'HowlWadaag', 'Wardhigley', 'Waaberi', 'HamarJajab', 'Bondhere', 'Karaan',
                                'Yaaqshid', 'Huriwaa', 'Kaxda', 'Hodan', 'Shibis', 'Abdiaziz', 'Shangani', 'Wadajir', 'HamarWeyne']
            Gender = ['Male', 'Female']
            context = {
            'districts': districts,
                'Genders': Gender,
                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Outpatient List',
                'Doctors': doctorList,
            }
            return render(request, 'Emergency/triage_list.html', context)
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

@login_required(login_url='Login')          
def intreatment_list(request):
    try:
        if request.user.has_perm('APEN.view_emergencyroomvisit'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            emergency_queue_list = []
            Status = "in-treatment"
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                emergency_queue_list = EmergencyRoomVisit.objects.filter(
                Q(Status__icontains="in-treatment")  &
                    Q(Patient__PatientFirstName__icontains=SearchQuery) 
                )
            else:
                emergency_queue_list = EmergencyRoomVisit.objects.filter()
                if request.user.is_superuser:
                    emergency_queue_list = EmergencyRoomVisit.objects.filter(
                        Q(Status__icontains="in-treatment")
                    ).order_by(
                        Case(
                            When(emergencytriage__TriageCategory="Immediate", then=1),
                            When(emergencytriage__TriageCategory="Emergent", then=2),
                            When(emergencytriage__TriageCategory="Urgent", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )
                else:
                    if "doctor" in request.user.employee.job_type.name.lower():
                        emergency_queue_list = EmergencyRoomVisit.objects.filter(
                        Q(Status__icontains="in-treatment") & ~Q(emergencytriage__Doctor__isnull=True) & Q(emergencytriage__Doctor=request.user.employee)
                        ).order_by(
                            Case(
                                When(emergencytriage__TriageCategory="Immediate", then=1),
                                When(emergencytriage__TriageCategory="Emergent", then=2),
                                When(emergencytriage__TriageCategory="Urgent", then=3),
                                default=4,
                                output_field=models.IntegerField(),
                            )
                        )
                  
            paginator = Paginator(emergency_queue_list, DataNumber)

            title_doctor = Title.objects.filter(name__icontains="Doctor")
            doctorList =[]
            for j in title_doctor:
                Doctor = Employee.objects.filter(job_type=j.id)
                for doc in Doctor:
                    doctorList.append(doc)
            
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            districts = ['Dharkenley', 'Deynile', 'HowlWadaag', 'Wardhigley', 'Waaberi', 'HamarJajab', 'Bondhere', 'Karaan',
                                'Yaaqshid', 'Huriwaa', 'Kaxda', 'Hodan', 'Shibis', 'Abdiaziz', 'Shangani', 'Wadajir', 'HamarWeyne']
            Gender = ['Male', 'Female']
            context = {
            'districts': districts,
                'Genders': Gender,
                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Outpatient List',
                'Doctors': doctorList,
                'Status':Status,
            }
            return render(request, 'Emergency/in-treatment-patients.html', context)
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

@login_required(login_url='Login')
def triage_form(request, pk):
    try:
        if request.user.has_perm('APEN.view_emergencytriage'):
            Emergency_visit = EmergencyRoomVisit.objects.get(pk=pk)
            chiefComplaint, allergic, Vitalsigns,  CurrentMedications, FamilyMedicalHistory, PastMedicalHistory, Assessment = [], [], [], [], [], [], []
            try:
                emergency_triage = EmergencyTriage.objects.get(Visit = pk)
                chiefComplaint = emergency_triage.ChiefComplaint.split(",")
                allergic = emergency_triage.Allergies.split(",")
                Vitalsigns = emergency_triage.Vitalsigns.split(",")
                CurrentMedications = emergency_triage.CurrentMedications.split(",")
                FamilyMedicalHistory = emergency_triage.FamilyMedicalHistory.split(",")
                PastMedicalHistory = emergency_triage.PastMedicalHistory.split(",")
                Assessment = emergency_triage.Assessment.split(",")

            except EmergencyTriage.DoesNotExist:
                emergency_triage = None

            examcategory = ExamCategory.objects.all()

            medicine_prescription = MedicinesPrescription.objects.filter(Visit = pk, Status = "Approved")
            medications_for_dropdown = MedicinePrescriptionDetials.objects.filter(PrescriptionNo__in=[medicine_name.id for medicine_name in medicine_prescription])
            medications_list = MedicationDose.objects.filter(Visit_id=pk)

            departments = Departments.objects.all()
            AssignedBed = AssignBed.objects.filter(Visit = pk)
            try:
                Isdischarged = Discharge.objects.get(Visit = pk)
            except Discharge.DoesNotExist:
                Isdischarged = None
            # passing for overview tab
            # for medicine prescriptions in overview
            Prescriped_medicines = MedicinesPrescription.objects.filter(Visit=pk)
            
            # for laboratory in overview
            ordered_laboratorities = LabTestOrders.objects.filter(Visit=pk)
            # for radiology in overview
            ordered_radiology = RadiologyOrders.objects.filter(Visit=pk)
            # for patient operation


            # # passing fo diagnosis
            # # for laboratory in diagnosis tab
            # for ordered_lab in ordered_laboratorities:
            #     lab_order_details = LabTestOrderDetails.objects.filter(LabTestOrder=ordered_lab.id)
                

            medicineCategories = Medicine_categories.objects.all()
            medicines = Medicine_categories.objects.all()
            medicineCategories = Medicine_categories.objects.all()
            labTests = LabTests.objects.all()
            radiologyExam = RadiologyExam.objects.all()
            examcategory = ExamCategory.objects.all()
            labgroups = LabTestGroups.objects.all()
            Status = "Approved"
            lab_order = LabTestOrders.objects.filter(Visit=pk)
            ordered_lab=""
            lab_result_list=[]
            lab_tests_list=[]
            lab_blood_result_list = []
            lab_parameter_result_list = []
            lab_blood_list = []
            lab_parameter_list = []
            unique_parameter_list = []
            unique_result_parameter_list = []
            blood_test_with_results_list = []
            test_group_list = []
            test_subgroup_list = []
            unique_group_list =[]
            unique_subgroup_list =[]
            unique_parameter_result_list =[]
            unique_types_list =[]
            unique_types =[]
            unique_blood =[]
            
            if lab_order:
                ordered_lab = LabTestOrders.objects.filter(Visit=pk)
                for lab in ordered_lab:
                    lab_result = LabTestResult.objects.filter(LabTestOrder_id=lab.id)
                    for laboratory_result in lab_result:
                        lab_result_list.append(laboratory_result)
                        lab_blood_results = Lab_Blood_Results.objects.filter(labTest_result=laboratory_result.id)
                        for lab_blood_result in lab_blood_results:
                            lab_blood_result_list.append(lab_blood_result)
                           
                            test_groups = LabTestGroups.objects.filter(id=lab_blood_result.TestID.Group.id)
                            for unique in test_groups:
                                test_group_list.append(unique.id)
                            test_subgroups = LabTestSubGroups.objects.filter(id=lab_blood_result.TestID.SubGroup.id)
                            for unique in test_subgroups:
                                test_subgroup_list.append(unique.id)
                        lab_parameter_results = Lab_ExaminationParameters_Results.objects.filter(labTest_result=laboratory_result.id)
                        for lab_parameter_result in lab_parameter_results:
                            lab_parameter_result_list.append(lab_parameter_result)
                            unique_parameter_result_list.append(lab_parameter_result.TestID.id)
                            unique_types_list.append(lab_parameter_result.Parameter.Type)
                    lab_details = LabTestOrderDetails.objects.filter(LabTestOrder=lab.id)
                    for lab_test in lab_details:
                        lab_tests_list.append(lab_test)
                        lab_blood = LabTest_Blood_Properties.objects.filter(TestID = lab_test.Test.id)
                        for l_blood in lab_blood:
                            lab_blood_list.append(l_blood.id)
                        lab_parameters = LabExaminationParameters.objects.filter(Test_id = lab_test.Test.id)
                        for l_param in lab_parameters:
                            lab_parameter_list.append(l_param.Test_id)
                            
           
            # for view lab 
            unique_parameter = set(lab_parameter_list)
            for u in unique_parameter:
                get_unique_parameter = LabExaminationParameters.objects.filter(Test_id=u)
                for unique in get_unique_parameter:
                    unique_parameter_list.append(unique)
            unique_result_parameter = set(unique_parameter_result_list)
            for u in unique_result_parameter:
                get_unique_result_parameter = LabTests.objects.filter(id=u)
                for unique in get_unique_result_parameter:
                    unique_result_parameter_list.append(unique)
            unique_groups = set(test_group_list)
            for unique in unique_groups:
                get_unique_group = LabTestGroups.objects.filter(id=unique)
                for group in get_unique_group:
                    unique_group_list.append(group)
            unique_subgroups = set(test_subgroup_list)
            for unique in unique_subgroups:
                get_unique_subgroup = LabTestSubGroups.objects.filter(id=unique)
                for subgroup in get_unique_subgroup:
                    unique_subgroup_list.append(subgroup)
            set_all_type = set(unique_types_list)
            for types in set_all_type:
                unique_types.append(types)
              
            set_unique_lab_blood = set(lab_blood_list)
            for unique in set_unique_lab_blood:
                get_unique_lab_blood = LabTest_Blood_Properties.objects.filter(id=unique)
                for unique_b in get_unique_lab_blood:
                    unique_blood.append(unique_b)
                
            RadiologyOrder = RadiologyOrders.objects.filter(Visit=pk)
            ordered_radio=""
            radio_result_list=[]
            radiology_exams = [] # passing for View prescription
            radio_result_details_list = []
            if RadiologyOrder:
                ordered_radio = RadiologyOrders.objects.filter(Visit=pk)
                for radio in ordered_radio:
                    radio_result = RadiologyResult.objects.filter(RadiologyOrder_id=radio.id)
                    for radiology_result in radio_result:
                        radio_result_list.append(radiology_result)
                        radio_result_details = RadiologyResultDetails.objects.filter(Radiology_Result=radiology_result.id)
                        for radio_result_detail in radio_result_details:
                            radio_result_details_list.append(radio_result_detail)
                    radiology_details = RadiologyOrderDetails.objects.filter(RadiologyOrder=radio.id)
                    for radiology in radiology_details:
                        radiology_exams.append(radiology)
            
            
            #for prescriptions
            prescriped_medicine_details_list =[]
            Prescriped_medicine = MedicinesPrescription.objects.filter(Visit=pk)
            for prescripe in Prescriped_medicine:
                prescriped_medicine_details = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=prescripe)
                for p in prescriped_medicine_details:
                    prescriped_medicine_details_list.append(p)
        
           
            # I'm pasing all employees bcz jobtype is not ready yet so can't do filter
            Employees = Employee.objects.all()
            # for Patient's Operations Table
            
            
    
           
            # for diagnosis view
            blood_properties = LabTest_Blood_Properties.objects.all()
            
            context = {
                'id': pk,
                'Emergency_visit':Emergency_visit,
            
                'examcategory':examcategory,
                'Medicines': medicines,
                'medications_list':medications_for_dropdown,
                'medications':medications_list,
                'departments':departments,
                'AssignedBed':AssignedBed,
                'Isdischarged':Isdischarged,

                #for triage form before and after submit
                'emergency_triage': emergency_triage,
                'chiefComplaint': chiefComplaint,
                'allergic': allergic,
                'Vitalsigns': Vitalsigns,
                'CurrentMedications': CurrentMedications,
                'FamilyMedicalHistory': FamilyMedicalHistory,
                'PastMedicalHistory': PastMedicalHistory,
                'Assessment': Assessment,
                # ----start passing for overview tab
                # for medicine prescriptions in overview
                'Prescriped_medicines': Prescriped_medicines,
                # for laboratory in overview
                'ordered_laboratorities': ordered_laboratorities,
                # for radiology in overview
                'ordered_radiology': ordered_radiology,
                # for patient operation in overview
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
               
                # 'Appointment': AppointmentId,
                'LabTests': labTests,
                'RadiologyExam': radiologyExam,
                'labgroups':labgroups,
                'examcategory':examcategory,
                # 'Patient': Patient,
                'blood_properties':blood_properties,
                'ordered_radio': ordered_radio,
                'ordered_lab': ordered_lab,
                'lab_result': lab_result_list,
                'radio_result': radio_result_list,
                'Status': Status,
              
                'Employees': Employees,
                
                
                
                #passing for prescriped medicine
                'Prescriped_medicine_details': prescriped_medicine_details_list,
                'Prescriped_medicine':Prescriped_medicine,
                
                #passing for view lab tests and results
                'ordered_lab_tests_list':lab_tests_list,
                'lab_blood_result_list':lab_blood_result_list,
                'lab_parameter_result_list':lab_parameter_result_list,
                'blood_test_with_results_list':blood_test_with_results_list,
                'lab_blood_list':unique_blood,
                'lab_parameter_list':lab_parameter_list,
                'unique_group_list':unique_group_list,
                'unique_subgroup_list':unique_subgroup_list,
                'unique_result_parameter_list':unique_result_parameter_list,
                'unique_types':unique_types,
                #passing for view radiology exams and result
                'radio_result_details_list' :radio_result_details_list,
                'radiology_exams' : radiology_exams,


                
            }
            return render(request, 'Emergency/triage_form.html', context)
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

@login_required(login_url='Login')
def manage_emergency_profile(request, action):
    try:
        if request.method == 'POST':
            if action == "new_triage_form":
                if request.user.has_perm('APEN.add_emergencytriage'):
                    # Get all data from the request
                    emergency_visit_id = request.POST.get('emergency_visit_id')

                    bloodPressure = request.POST.get('bloodPressure')
                    HeartRate = request.POST.get('HeartRate')
                    RespiratoryRate = request.POST.get('RespiratoryRate')
                    Temperature = request.POST.get('Temperature')

                    triageDate = request.POST.get('triageDate')
                    triageCategory = request.POST.get('triageCategory')
                    cheifComplaint = request.POST.get('cheifComplaint')
                    Allergies = request.POST.get('Allergies')
                    Medications = request.POST.get('Medications')
                    pastHistory = request.POST.get('pastHistory')
                    familyHistory = request.POST.get('familyHistory')
                    IsDoctorRequired = request.POST.get('IsDoctorRequired')
                    Assessment = request.POST.get('Assessment')
                    Doctor = request.POST.get('Doctor')
                    Comments = request.POST.get('Comments')

                    PatientFirstName = request.POST.get('PatientFirstName')
                    PatientMiddleName = request.POST.get('PatientMiddleName')
                    PatientLastName = request.POST.get('PatientLastName')
                    PatientAge = request.POST.get('PatientAge')
                    PatientVillage = request.POST.get('PatientVillage')
                    PatientGender = request.POST.get('PatientGender')
                    PatientMobileNo = request.POST.get('PatientMobileNo')
                    PatientDistrict = request.POST.get('PatientDistrict')
                    EmergencyName = request.POST.get('EmergencyName')
                    EmergencyNumber = request.POST.get('EmergencyNumber')

                    if PatientFirstName == '' or PatientFirstName == 'null' or PatientFirstName is None or PatientFirstName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s First Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(PatientFirstName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for patient first name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if PatientMiddleName == '' or PatientMiddleName == 'null' or PatientMiddleName is None or PatientMiddleName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Father Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(PatientMiddleName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only patient middle name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if PatientLastName == '' or PatientLastName == 'null' or PatientLastName is None or PatientLastName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Last Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validation(PatientLastName) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for patient lastname',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if PatientAge == '' or PatientAge == 'null' or PatientAge is None or PatientAge == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Age',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if number_validation(PatientAge) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text and nums only for patient age',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if PatientVillage !='':
                        if text_validationNumber(PatientVillage) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text and nums only for patient Village',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                
                    if len(PatientMobileNo) >=1:
                        if number_validation(PatientMobileNo) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter numbers only for Mobile Number',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                    if EmergencyNumber !='':
                        if number_validation(EmergencyNumber) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter numbers only for Emergency Number',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if EmergencyName !='':
                        if text_validation(EmergencyName) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter numbers only for emergency Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                
                    if PatientGender == '' or PatientGender == 'null' or PatientGender is None or PatientGender == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Patient Gender',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if bloodPressure == '' or bloodPressure == 'null' or bloodPressure is None or bloodPressure == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s BLood Pressure',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if vitalsigns_text_numberValidation(bloodPressure) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for blood pressure',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if HeartRate == '' or HeartRate == 'null' or HeartRate is None or HeartRate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Heart rate',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if vitalsigns_text_numberValidation(HeartRate) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for heart rate',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if RespiratoryRate == '' or RespiratoryRate == 'null' or RespiratoryRate is None or RespiratoryRate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Respiratory Rate',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if vitalsigns_text_numberValidation(RespiratoryRate) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter text only for respiratory rate',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Temperature == '' or Temperature == 'null' or Temperature is None or Temperature == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Patient\'s Temparature',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if vitalsigns_text_numberValidation(Temperature) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for temperature',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if cheifComplaint == '' or cheifComplaint == 'null' or cheifComplaint is None or cheifComplaint == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'add chief Complaint',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Comments != '' :
                        if text_validationNumber(Comments) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for comments',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        Comments = 'None'
                    if Allergies != '' :
                        if text_validationNumber(Allergies) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for Allergies',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        Allergies = 'None'
                    if familyHistory != '' :
                        if text_validationNumber(familyHistory) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for family medical history',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        familyHistory = 'None'
                    if Medications != '' :
                        if text_validationNumber(Medications) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for current medications',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        Medications = 'None'
                    if pastHistory != '' :
                        if text_validationNumber(pastHistory) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for medical history',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        pastHistory = 'None'
                    if Assessment == '' or Assessment == 'null' or Assessment is None or Assessment == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Enter Assessment',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validationNumber(Assessment) == False:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter valid text for Nurse Assessment',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                

                    if triageDate == '' or triageDate == 'null' or triageDate is None or triageDate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Triage date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if triageCategory == '' or triageCategory == 'null' or triageCategory is None or triageCategory == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select a triage category',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Doctor == '' or Doctor == 'null' or Doctor is None or Doctor == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Doctor',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    PatientFirstName = RemoveSpecialCharacters(PatientFirstName)
                    PatientMiddleName = RemoveSpecialCharacters(PatientMiddleName)
                    PatientLastName = RemoveSpecialCharacters(PatientLastName)
                    PatientAge = RemoveSpecialCharacters(PatientAge)
                    PatientVillage = RemoveSpecialCharacters(PatientVillage)
                    PatientMobileNo = RemoveSpecialCharacters(PatientMobileNo)
                
                    new_emergency_patient = Patients(PatientFirstName=PatientFirstName, PatientMiddleName=PatientMiddleName, PatientLastName=PatientLastName, PatientAge=PatientAge, PatientVillage=PatientVillage,
                                                PatientGender=PatientGender, PatientMobileNo=PatientMobileNo, PatientDistrict=PatientDistrict)
                    new_emergency_patient.save()
                    current_patient = Patients.objects.get(id = new_emergency_patient.id)
                    new_visit = EmergencyRoomVisit(VisitNumber = GenerateVisitNumber(),Patient_id=current_patient.id, EmergencyName=EmergencyName, EmergencyNumber=EmergencyNumber, Status = "Pending")
                    new_visit.save()
                
                
                    triageNurse = Users.objects.get(id=request.user.id)
                    vitalsign = f'{bloodPressure}, {HeartRate}, {RespiratoryRate},{Temperature}'
                    emergency_visit = EmergencyRoomVisit.objects.get(id=new_visit.id)
                   
                    doctor =Employee.objects.get(id=Doctor)
                    triage_table = EmergencyTriage(Visit_id=emergency_visit.id, Vitalsigns=vitalsign, ChiefComplaint=cheifComplaint, Allergies=Allergies, CurrentMedications=Medications, FamilyMedicalHistory=familyHistory,
                                        Triage_dateTime=triageDate, PastMedicalHistory=pastHistory, Doctor_id=doctor.id, TriageCategory=triageCategory, Assessment=Assessment, TriageNurse_id=triageNurse.id, Comment=Comments)
                    triage_table.save()
                    emergency_visit.Status = "in-queue"
                    emergency_visit.save()
                   
                
                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Triage form has been created',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to add a triage',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'new_medicine_dose':
                if request.user.has_perm('APEN.add_medicationdose'):
                    # Get all data from the request
                    emergency_visit_id = request.POST.get('emergency_visit_id')
                    MedicationsDose_date = request.POST.get('MedicationsDose_date')
                    MedicationsName = request.POST.get('MedicationsName')
                    MedicationsDose_time = request.POST.get('MedicationsDose_time')
                    Medication_dose = request.POST.get('MedicationDose')
                    Remarks = request.POST.get('Remarks')
 

                    if MedicationsDose_date == '' or MedicationsDose_date == 'null' or MedicationsDose_date is None or MedicationsDose_date == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Medicine Dose',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if MedicationsName == '' or MedicationsName == 'null' or MedicationsName is None or MedicationsName == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Medicine Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if MedicationsDose_time == '' or MedicationsDose_time == 'null' or MedicationsDose_time is None or MedicationsDose_time == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Medicine Dose Time',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if Medication_dose == '' or Medication_dose == 'null' or Medication_dose is None or Medication_dose == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Enter Medicine Dose',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                
                    if Remarks != '' :
                            if text_validationNumber(Remarks) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for Remarks',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    else:
                        Remarks = 'None'
                   
                    
                    Remarks = RemoveSpecialCharacters(Remarks)
                    medicine_name = MedicinePrescriptionDetials.objects.get(id = MedicationsName)
                    visit = EmergencyRoomVisit.objects.get(id=emergency_visit_id)
                    new_medicine_dose = MedicationDose(Visit_id = visit.id, Medication_date=MedicationsDose_date, Medicition_time=MedicationsDose_time, Medication_name=medicine_name, Medication_dose=Medication_dose, Medicition_Remarks=Remarks) 
                    new_medicine_dose.save()
                
                    # username = request.user.username
                    # names = request.user.first_name + ' ' + request.user.last_name
                    # avatar = str(request.user.avatar)
                    # module = "Patient/ Emergency module"
                    # action = f'{names} ayaa diwaan geliye Bukaan cusub oo magaciisu yahay {PatientFirstName} {PatientMiddleName}  {PatientLastName}'
                    # path = request.path
                    # sendTrials(request, username, names,
                    #         avatar, action, module, path)

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New Medicine Dose has been given',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )      
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to add medicine dose',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            
            if action == "get_bed_room":
                if request.user.has_perm('APEN.add_assignbed'):
                    room_id = request.POST.get('room')
                
                    get_bed = Beds.objects.filter(
                        Room=room_id, status = "Available")
                    # get_dep_section = Sections.objects.filter(departments = depart_id)
                    # base_pay = 0

                    message = []
                    for xbed in range(0, len(get_bed)):

                        message.append({
                            'id': get_bed[xbed].id,
                            'name': get_bed[xbed].BedNO,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')    
            if action == "get_room_department":
                if request.user.has_perm('APEN.add_assignbed'):
                    departments = request.POST.get('departments')
                
                    get_room_category = Room_category.objects.filter(
                        department=departments)
                    
                   
                    Status = "availible"
                    rooms = Room.objects.filter(Room_category=room_category.id, status=Status)

                    message = []
                    for x_room in range(0, len(rooms)):
                        message.append({
                            'id': rooms[x_room].id,
                            'name': rooms[x_room].Room_NO,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == 'assign_bed':
                if request.user.has_perm('APEN.add_assignbed'):
                    # Get all data from the request
                    emergency_visit_id = request.POST.get('emergency_visit_id')
                    room = request.POST.get('room')
                    bed = request.POST.get('bed')
                    bed_date = request.POST.get('bed_date')
                

                    if room == '' or room == 'null' or room is None or room == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select room',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if bed == '' or bed == 'null' or bed is None or bed == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select bed',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if bed_date == '' or bed_date == 'null' or bed_date is None or bed_date == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select bed arrival date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    rooms = Room.objects.get(id = room)
                    beds = Beds.objects.get(id = bed)

                    Assign_Bed = AssignBed(Room_id=rooms.id, Bed_id=beds.id, FromDate=bed_date, Visit_id = emergency_visit_id) 
                    Assign_Bed.save()

                    beds.status = "Occupied"
                    beds.save() 
                    all_beds_full = Beds.objects.filter(Room=rooms, status='Occupied').count()
                    all_beds_in_room =rooms.beds_set.count()
                    if all_beds_in_room == all_beds_full:
                        rooms.status = 'full'
                        rooms.save()
                    else:
                        rooms.status = 'availible'
                        rooms.save()

                    
                
                    # username = request.user.username
                    # names = request.user.first_name + ' ' + request.user.last_name
                    # avatar = str(request.user.avatar)
                    # module = "Patient/ Emergency module"
                    # action = f'{names} ayaa diwaan geliye Bukaan cusub oo magaciisu yahay {PatientFirstName} {PatientMiddleName}  {PatientLastName}'
                    # path = request.path
                    # sendTrials(request, username, names,
                    #         avatar, action, module, path)

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'New bed has been Assigned',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )      
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to assign a bed',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == 'new_discharge':
                if request.user.has_perm('APEN.add_discharge'):
                    # Get all data from the request
                    emergency_visit_id = request.POST.get('emergency_visit_id')

                    discharge_date = request.POST.get('discharge_date')
                    dischargeStatus = request.POST.get('dischargeStatus')

                    admission_date = request.POST.get('admission_date')
                    bedType = request.POST.get('bedType')
                    patient_priority = request.POST.get('patient_priority')
                    admission_reason = request.POST.get('admission_reason')
                    admission_note = request.POST.get('admission_note')

                    diagnosis_result = request.POST.get('diagnosis_result')
                    surgery_operations = request.POST.get('surgery_operations')
                    discharge_note = request.POST.get('discharge_note')

                    referel_date = request.POST.get('referel_date')
                    hospital_name = request.POST.get('hospital_name')
                    referel_reason = request.POST.get('referel_reason')

                    death_date = request.POST.get('death_date')
                    death_reason = request.POST.get('death_reason')
                    

                    if discharge_date == '' or discharge_date == 'null' or discharge_date is None or discharge_date == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select discharge date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if dischargeStatus == '' or dischargeStatus == 'null' or dischargeStatus is None or dischargeStatus == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Dischagre Status',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if dischargeStatus == "Admitted":
                        if bedType == '' or bedType == 'null' or bedType is None or bedType == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Select Bed Type',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if admission_date == '' or admission_date == 'null' or admission_date is None or admission_date == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Select Admission Date',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                        if patient_priority == '' or patient_priority == 'null' or patient_priority is None or patient_priority == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter select patient priority',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                        if admission_reason != '' :
                                if text_validationNumber(admission_reason) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': 'Please enter valid text for admission reason',
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                        else:
                            admission_reason = 'None'
                        if admission_note != '' :
                            if text_validationNumber(admission_note) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for admission reason',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                        else:
                            admission_note = 'None'



                        
                    if diagnosis_result != '' :
                        if text_validationNumber(diagnosis_result) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for admission reason',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        diagnosis_result = 'None'

                    if surgery_operations != '' :
                        if text_validationNumber(surgery_operations) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for admission reason',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        surgery_operations = 'None'
                    if discharge_note != '' :
                        if text_validationNumber(discharge_note) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for admission reason',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        discharge_note = 'None'

                    if dischargeStatus == "Referrel":
                        if referel_date == '' or referel_date == 'null' or referel_date is None or referel_date == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Select referel date',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        

                        if hospital_name == '' or hospital_name == 'null' or hospital_name is None or hospital_name == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Hospital Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if text_validationNumber(hospital_name) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for admission reason',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                        if referel_reason != '' :
                            if text_validationNumber(referel_reason) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for admission reason',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                        else:
                            referel_reason = 'None'
                    if dischargeStatus == "Death":
                        if death_date == '' or death_date == 'null' or death_date is None or death_date == 'undefined':
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Select referel date',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        if death_reason != '' :
                            if text_validationNumber(death_reason) == False:
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for admission reason',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                        else:
                            death_reason = 'None'

                    admission_reason = RemoveSpecialCharacters(admission_reason)
                    admission_note = RemoveSpecialCharacters(admission_note)
                    diagnosis_result = RemoveSpecialCharacters(diagnosis_result)
                    surgery_operations = RemoveSpecialCharacters(surgery_operations)
                    discharge_note = RemoveSpecialCharacters(discharge_note)
                    death_reason = RemoveSpecialCharacters(death_reason)
                    referel_reason = RemoveSpecialCharacters(referel_reason)

                    visit = EmergencyRoomVisit.objects.get(id=emergency_visit_id)
                
                    if dischargeStatus == "Referrel":
                        new_referel_patient = Referrel(HospitalName = hospital_name, Referel_Date=referel_date, Referel_Reason=referel_reason)
                        new_referel_patient.save()
                        current_referel = Referrel.objects.get(id=new_referel_patient.id)
                        new_dischagre_referel = Discharge(Visit_id=visit.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result, referrel_id= current_referel.id) 
                        new_dischagre_referel.save()
                    elif dischargeStatus == "Normal":
                        new_dischagre_normal = Discharge(Visit_id=visit.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result) 
                        new_dischagre_normal.save()
                    elif dischargeStatus == "Death":  
                        new_death_patient = PatientDeath(Death_Date = death_date, Death_Reason=death_reason)
                        new_death_patient.save()
                        current_death = PatientDeath.objects.get(id=new_death_patient.id)
                        new_dischagre_death = Discharge(Visit_id=visit.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result, death_id= current_death.id) 
                        new_dischagre_death.save()
                    elif dischargeStatus == "Admitted":  
                        new_order = AdmissionOrder(Visit_id = visit.id, Ordered_by = "Emergency Department", AdmissionDate= admission_date, AdmissionReason=admission_reason, BedType=bedType, Status="Pending", Note=admission_note, patient_priority=patient_priority )
                        new_order.save()
                        current_order = AdmissionOrder.objects.get(id=new_order.id)
                        new_dischagre_admission = Discharge(Visit_id=visit.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result, Admission_order_id= current_order.id) 
                        new_dischagre_admission.save()

                    else:
                        return render(request, 'Hr/404.html')
                    
                    try:
                        assigned_bed = AssignBed.objects.get(Visit_id=visit.id)
                        assigned_bed.ToDate = discharge_date
                        assigned_bed.save()

                        update_bed  =Beds.objects.get(id=assigned_bed.Bed.id)
                        update_bed.status = "Available"
                        update_bed.save()
                        room_id = Room.objects.get(id=assigned_bed.Room.id)
                        all_beds_full = Beds.objects.filter(Room=room_id, status='Occupied').count()
                        all_beds_in_room =room_id.beds_set.count()
                        if all_beds_in_room == all_beds_full:
                            room_id.status = 'full'
                            room_id.save()
                        else:
                            room_id.status = 'availible'
                            room_id.save()
                    except AssignBed.DoesNotExist:
                        pass
                

                    visit.DischargeDateTime = discharge_date
                    visit.Status = "Discharged"
                    visit.save()

                    # username = request.user.username 
                    # names = request.user.first_name + ' ' + request.user.last_name
                    # avatar = str(request.user.avatar)
                    # module = "Patient/ Emergency module"
                    # action = f'{names} ayaa diwaan geliye Bukaan cusub oo magaciisu yahay {PatientFirstName} {PatientMiddleName}  {PatientLastName}'
                    # path = request.path
                    # sendTrials(request, username, names,
                    #         avatar, action, module, path)

                    return JsonResponse(
                        {
                            'isError': False,
                            'Message': 'a Patient has been succesfully discharged',
                            'title': 'Masha Allah!',
                            'type': 'success+',
                        }
                    )      
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to discharge a patient',
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
def manage_patient_diagnosis(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_diagnosis':
                if request.user.has_perm('APEN.add_labtestorders') or request.user.has_perm('APEN.add_radiologyorders'):
                    emergency_visit_id = request.POST.get('emergency_visit_id')
                    laboratory = request.POST.get('laboratory')
                    radiology = request.POST.get('radiology')
                    visit = EmergencyRoomVisit.objects.get(id=emergency_visit_id)
                    Status = "Pending"
                    if laboratory or radiology:
                        if laboratory:
                            laboratory = [x for x in laboratory.split(',')]
                            if laboratory == '' or laboratory == 'null' or laboratory is None or laboratory == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Select Laboratory',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                                
                            new_lab_order = LabTestOrders(Visit_id = visit.id,TestOrderNumber=GenerateTestOrderNumber(), Ordered_by = "Emergency Department", Status=Status)
                            new_lab_order.save()
                            # save lab order details using current lab order id
                            current_lab_order = LabTestOrders.objects.get(pk=new_lab_order.id)
                            for lab in laboratory:
                                get_labTests = LabTests.objects.get(id=lab)
                                new_labTest_order_details = LabTestOrderDetails(LabTestOrder_id=current_lab_order.id, Test_id=get_labTests.id)
                                new_labTest_order_details.save()

                        if radiology:
                            radiology = [x for x in radiology.split(',')]
                            if radiology == '' or radiology == 'null' or radiology is None or radiology == 'undefined':
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': 'Select Radiology',
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                            # save radiology exam orders
                            new_radiology_order = RadiologyOrders(Visit_id = visit.id,RadiologyOrderNumber=GenerateRadiologyOrderNumber(), Ordered_by = "Emergency Department" ,Status=Status)
                            new_radiology_order.save()
                            # save radiology exam order details
                            current_radiology_order = RadiologyOrders.objects.get(pk=new_radiology_order.id)
                            for radio in radiology:
                                get_radiologyExam = RadiologyExam.objects.get(id=radio)
                                new_radiologyExam_order_details = RadiologyOrderDetails(RadiologyOrder_id=current_radiology_order.id,  RadiologyExam_id=get_radiologyExam.id)
                                new_radiologyExam_order_details.save()
                        return JsonResponse(
                            {
                                'isError': False,
                                'Message': 'New Diagnosis has been created',
                                'title': 'Masha Allah !',
                                'type': 'success+',
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'please Select one of the diagnosis ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to add diagnosis',
                            'title': 'Access is Denied !',
                            'type': 'warning',
                        },
                    )
            if action == "get_category_radiology":
                if request.user.has_perm('APEN.add_radiologyorders'):
                    categoryid = request.POST.get('radiologyCategory')
                    print(categoryid)
                    get_radiology_id = RadiologyExam.objects.filter(Category_id=categoryid)
                    message = []
                    for xradio in range(0, len(get_radiology_id)):

                        message.append({
                            'id': get_radiology_id[xradio].id,
                            'name': get_radiology_id[xradio].ExamName,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_radiology_option_data":
                if request.user.has_perm('APEN.add_radiologyorders'):
                    radiology_exam = RadiologyExam.objects.all()
                    radiology_category = ExamCategory.objects.all()
                    radiology_list = []
                    radiology_category_list = []
                    for index, item in enumerate(radiology_category):
                        radiology_category_list.append({
                            'id': item.id,
                            'name': item.CategoryName,
                        })
                    for index, item in enumerate(radiology_exam):
                        radiology_list.append({
                            'id': item.id,
                            'name': item.ExamName,
                        })
                        
                
                    message = {
                        'radiology': radiology_list,
                        'radiology_category': radiology_category_list,
                    
                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_laboratory_option_data":
                if request.user.has_perm('APEN.add_labtestorders'):
                    laboratory_test = LabTests.objects.all()
                    lab_group = LabTestGroups.objects.all()
                    laboratory_test_list = []
                    lab_group_list = []
                    for index, item in enumerate(laboratory_test):
                        laboratory_test_list.append({
                            'id': item.id,
                            'name': item.TestName,
                        })
                    for index, item in enumerate(lab_group):
                        lab_group_list.append({
                            'id': item.id,
                            'name': item.GroupName,
                        })
                    
                    message = {
                        
                        'laboratory_test': laboratory_test_list,
                        'lab_group': lab_group_list,
                    }

                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_category_lab":
                if request.user.has_perm('APEN.add_labtestorders'):
                    sample = request.POST.get('Sample1')
                    all_groups =[]
                    message = []
                    get_test_id = LabTests.objects.filter(SampleType=sample)
                    get_groups =LabTestGroups.objects.filter(sampleType=sample)
                    for xgroup in range(0, len(get_groups)):
                        all_groups.append({
                            'id': get_groups[xgroup].id,
                            'name': get_groups[xgroup].GroupName,
                        })
                        
                    for xlab in range(0, len(get_test_id)):
                        message.append({
                            'id': get_test_id[xlab].id,
                            'name': get_test_id[xlab].TestName,
                        })
                    return JsonResponse({'isError': False, 'Message': message, 'Groups':all_groups}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_blood_test":
                if request.user.has_perm('APEN.add_labtestorders'):
                    group_id = request.POST.get('Group')
                    message = []
                    get_lab = LabTest_Blood_Properties.objects.filter(Group=group_id)
                    
                    for xlab in range(0, len(get_lab)):
                        message.append({
                            'id': get_lab[xlab].TestID.id,
                            'name': get_lab[xlab].TestID.TestName,
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
def manage_prescription(request, action):
    try: 
        if request.method == 'POST':
            if action == 'new_prescription':
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    emergency_visit_id = request.POST.get('emergency_visit_id')
                    MedicineCategory = request.POST.get('MedicineCategory1')
                    medicine = request.POST.get('Medicine1')
                    Dose = request.POST.get('Dose1')
                    DoseInterval = request.POST.get('DoseInterval1')
                    DoseDuration = request.POST.get('DoseDuration1')
                    Quantity = request.POST.get('Qty1')
                    AvailableQty1 = request.POST.get('AvailableQty1')
                    Instructions = request.POST.get('Instructions')

                    if MedicineCategory:
                        
                        MedicineCategory = [x for x in MedicineCategory.split(',')]
                        for med_category in range(0, len(MedicineCategory )):
                            if MedicineCategory[med_category] == '' or MedicineCategory[med_category]== 'null' or MedicineCategory[med_category] is None or MedicineCategory[med_category] == 'undefined':
                                return JsonResponse(
                                    {
                                    'isError': True,
                                    'Message': 'Enter Medicine Category',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        
                    
                        medicine = [x for x in medicine.split(',')]
                        for medicine_len in range(0, len(medicine )):
                            if medicine[medicine_len] == '' or medicine[medicine_len] == 'null' or medicine[medicine_len] is None or medicine[medicine_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Enter Medicine',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                
                        
                        Dose = [x for x in Dose.split(',')]
                        for dose_len in range(0, len(Dose )):
                            if Dose[dose_len] == '' or Dose[dose_len] == 'null' or Dose[dose_len] is None or Dose[dose_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Enter Dose',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    
                        DoseInterval = [x for x in DoseInterval.split(',')]
                        for dose_interval_len in range(0, len(DoseInterval )):
                            if DoseInterval[dose_interval_len] == '' or DoseInterval[dose_interval_len] == 'null' or DoseInterval[dose_interval_len] is None or DoseInterval[dose_interval_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Select Dose Interval',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                    
                        
                    
                        DoseDuration = [x for x in DoseDuration.split(',')]
                        for dose_duration_len in range(0, len(DoseDuration )):
                            if DoseDuration[dose_duration_len] == '' or DoseDuration[dose_duration_len] == 'null' or DoseDuration[dose_duration_len] is None or DoseDuration[dose_duration_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Select Dose Duration',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                            )
                    
                        
                        
                    
                        AvailableQty1 = [int(x) for x in AvailableQty1.split(',')]
                        Quantity = [int(x) for x in Quantity.split(',')]
                        for quantity_len in range(0, len(Quantity )):
                            if Quantity[quantity_len] == '' or Quantity[quantity_len] == 'null' or Quantity[quantity_len] is None or Quantity[quantity_len] == 'undefined':
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Select Quantity',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                           
                            if Quantity[quantity_len] > AvailableQty1[quantity_len]:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Quantity prescribed exceeds pharmacy stock. Please adjust prescription.',
                                        'title': 'Quantity Mismatch!',
                                        'type': 'warning',
                                    }
                                )
                        if Instructions != '' :
                            if text_validationNumber(Instructions) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for Instructions',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                        else:
                            Instructions = 'None'
                        Instructions = RemoveSpecialCharacters(Instructions)
                        visit = EmergencyRoomVisit.objects.get(id=emergency_visit_id)
                        if visit.Status == "in-queue":
                            return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please first approve patient before you Prescribe a medicine',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                        else:
                            Status = "Pending"
                            # save medicine prescription 
                            new_medicine_prescription = MedicinesPrescription(instructions = Instructions, Visit_id = visit.id, PrescriptionNo=outpatient.GeneratePrescriptionNumber(), Ordered_by = "Emergency Department", Status=Status)
                            new_medicine_prescription.save()
                            # save medicines prescription details using medicine prescription order ID
                            Current_medicine_prescription = MedicinesPrescription.objects.get(pk=new_medicine_prescription.id)
                            for (med, dose, dose_interval, dose_duration, quantity) in zip(medicine, Dose, DoseInterval, DoseDuration, Quantity):
                                medicinetransection_id = Medicine.objects.get(id=med)
                                get_medicine = pharmacy_medicine.objects.get(Medicine_name= medicinetransection_id.id)
                                new_medicine_prescription_details = MedicinePrescriptionDetials(PrescriptionNo_id=Current_medicine_prescription.id, MedicineName=get_medicine, Quantity=quantity, Dose=dose, DoseInterval=dose_interval, DoseDuration=dose_duration)
                                new_medicine_prescription_details.save()
                        
                        
                            return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'New Prescription has been created',
                                    'title': 'Masha Allah !',
                                    'type': 'success+',
                                }
                                )
                    else:
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Medicine Category',
                                'title': 'Validation Error!',
                                'type': 'warning',
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
            if action == 'edit_prescription':
                pass

            if action == "get_option_data":
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    medicines = pharmacy_medicine.objects.all()
                    medicines_category = pharmacy_medicine.objects.all()
                    medicine = []
                    medicine_category = []
                    for index, item in enumerate(medicines_category):
                        medicine_category.append({
                            'id': item.Medicine_categories.id,
                            'name': item.Medicine_categories.medicine_cat_name,
                        })
                    for index, item in enumerate(medicines):
                        medicine.append({
                            'id': item.id,
                            'name': item.Medicine_name.Medicine_name,
                        })
                    message = {
                        'medicines': medicine,
                        'medicines_category': medicine_category,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_category_medicine":
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    medicine_id = request.POST.get('MedicineCategory1')
                    get_medicine_id = pharmacy_medicine.objects.filter(
                        Medicine_categories=medicine_id)
                
                    message = []
                    for xmedicine in range(0, len(get_medicine_id)):

                        message.append({
                            'id': get_medicine_id[xmedicine].Medicine_name.id,
                            'name': get_medicine_id[xmedicine].Medicine_name.Medicine_name,
                            'total_quantity': get_medicine_id[xmedicine].Total_quantity,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_available_medicine":
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    medicine_id = request.POST.get('Medicine')
                    medicineid = Medicine.objects.get(id=medicine_id)
                    medicine = pharmacy_medicine.objects.filter(
                        Medicine_name=medicineid.id)
                    message = []
                    for xmedicine in range(0, len(medicine)):

                        message.append({
                        
                            'total_quantity': medicine[xmedicine].Total_quantity,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_medicine_category":
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    category = request.POST.get('MedicineCategory')
                    message = []
                    get_medicine = pharmacy_medicine.objects.filter(Medicine_categories_id	=category)
                    
                    for xmed in range(0, len(get_medicine)):
                        message.append({
                            'id': get_medicine[xmed].id,
                            'name': get_medicine[xmed].Medicine_name.MedId.Medicine_name,
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
def emergency_discharged_patients_list(request):
    try:
        if request.user.has_perm('APEN.view_discharge'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            CheckDischargeStatus = 'discharge_status' in request.GET
            dischrge_status = 'All'
            if CheckDischargeStatus:
                dischrge_status = request.GET['discharge_status']

            dataFiltering = {}
            if dischrge_status != 'All':
                dataFiltering['dischargeStatus'] = dischrge_status
                            
            DataNumber = 10
            SearchQuery = ''
            discharged_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                discharged_list = Discharge.objects.filter(
                    Q(Patient__get_e_full_name__icontains=SearchQuery),
                    **dataFiltering,


                )
            else:
               discharged_list = Discharge.objects.filter(Admission_id__isnull=True, **dataFiltering)

            paginator = Paginator(discharged_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
        
                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Dishcarged Patient List',
                'discharge_status':dischrge_status,
            }
            return render(request, 'Emergency/emergency-dishcarged-patients.html', context)
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
def approve_visit(request, action):
    try:
        if action == "approve_visit":
            if request.user.has_perm('APEN.Approve_visit'):
                # Get all data from the request
                emergency_visit_id = request.POST.get('emergency_visit_id')
                status = request.POST.get('status')
                update_visit = EmergencyRoomVisit.objects.get(id=emergency_visit_id)
                update_visit.Status = status
                update_visit.save()

                return JsonResponse(
                    {
                        'isError': False,
                        'Message': ' Approved Succesfully',
                        'title':  "The Visit has been",
                        'type': 'success',
                    }
                    )
            else:
                return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'You dont have permission to approve an emergency visit',
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
def GenerateVisitNumber():
    try:
        last_id = EmergencyRoomVisit.objects.filter(~Q(VisitNumber=None)).last()
        serial = 0
        today = datetime.today().strftime('%d/%m/%y')
        today_without_slashes = today.replace('/', '')
        if last_id is not None:
            serial = int(last_id.VisitNumber[8:])
        serial = serial + 1

        if serial < 10:
            serial = '000' + str(serial)
        elif serial < 100:
            serial = '00' + str(serial)
        elif serial < 1000:
            serial = '0' + str(serial)

        return f"VS{today_without_slashes}{serial}"
    except Exception as error:
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)