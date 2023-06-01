from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from APEN.outpatient import GeneratePrescriptionNumber
from django.db.models import Sum
from Hr.views import RemoveSpecialCharacters, number_validation, text_validation, text_validationNumber
from LRPD.LabResult import GenerateTestOrderNumber
from LRPD.radiology import GenerateRadiologyOrderNumber
from .models import *
from Hr.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Inventory.models import Medicine, Medicine_categories, MedicineTransection
from LRPD.models import LabTests, LabTestOrders, RadiologyExam, RadiologyOrders, LabTestOrderDetails, RadiologyOrderDetails, LabTestResult, RadiologyResult,pharmacy_medicine
from LRPD.models import *
from Users.models import Users
from django.contrib.auth.decorators import permission_required
from Users.models import sendException
from Users.views import sendTrials
from django.db.models import Case, When

@login_required(login_url='Login')
def ordered_admissions(request):
    try:
        if request.user.has_perm('APEN.view_admissionorder'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            inpatient_orders_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                inpatient_orders_list = Appointments.objects.filter(
                    Q(Patient__get_fullName__icontains=SearchQuery) |
                    Q(Doctor__first_name__icontains=SearchQuery)

                )
            else:
                inpatient_orders_list = AdmissionOrder.objects.filter(Status="Pending").order_by(
                        Case(
                            When(patient_priority="Emergency", then=1),
                            When(patient_priority="Urgent", then=2),
                            When(patient_priority="nonUrgent", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )

            paginator = Paginator(inpatient_orders_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            room_category = Room_category.objects.all()
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Outpatient List',
                'room_category': room_category,
            }
            return render(request, 'Patients/ordered_admissions.html', context)
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
def manage_ordered_admissions(request, action):
    try:
        if request.method == 'POST':
            if action == "get_ordered_admission":
                if request.user.has_perm('APEN.add_admissionorder'):
                    id = request.POST.get('orderid')
                    
                    orderedAdmission = AdmissionOrder.objects.get(id = id)
                    
                    if orderedAdmission.Appointment:
    
                        message = {
                            'OrderId': orderedAdmission.id,
                            'patientFullname':orderedAdmission.Appointment.Patient.get_fullName(),
                            'PatientAge': orderedAdmission.Appointment.Patient.PatientAge,
                            'PatientGender': orderedAdmission.Appointment.Patient.PatientGender,
                            'PatientMobileNo': orderedAdmission.Appointment.Patient.PatientMobileNo,
                            'PatientDistrict': orderedAdmission.Appointment.Patient.PatientDistrict,
                            'PatientVillage': orderedAdmission.Appointment.Patient.PatientVillage,
                            'Doctor': orderedAdmission.Appointment.Doctor.get_full_name(),
                            'admissionDate': orderedAdmission.AdmissionDate,
                            'orderedBy': orderedAdmission.Ordered_by,
                            'Note': orderedAdmission.Note,
                            'admissonReason': orderedAdmission.AdmissionReason,
                            'patientPriority': orderedAdmission.patient_priority,
                            
                        }
                    elif orderedAdmission.Visit:
                        message = {
                                'OrderId': orderedAdmission.id,
                                'patientFullname':orderedAdmission.Visit.Patient.get_fullName(),
                                'PatientAge': orderedAdmission.Visit.Patient.PatientAge,
                                'PatientGender': orderedAdmission.Visit.Patient.PatientGender,
                                'PatientMobileNo': orderedAdmission.Visit.Patient.PatientMobileNo,
                                'PatientDistrict': orderedAdmission.Visit.Patient.PatientDistrict,
                                'PatientVillage': orderedAdmission.Visit.Patient.PatientVillage,
                                'Doctor' : orderedAdmission.Visit.emergencytriage_set.first().Doctor.get_full_name(),
                                'admissionDate': orderedAdmission.AdmissionDate,
                                'orderedBy': orderedAdmission.Ordered_by,
                                'Note': orderedAdmission.Note,
                                'admissonReason': orderedAdmission.AdmissionReason,
                                'patientPriority': orderedAdmission.patient_priority,
                            }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_room_category":
                if request.user.has_perm('APEN.add_admissionorder'):
                    room_category_id = request.POST.get('Room_category')
                
                    room_category = Room_category.objects.get(
                        id=room_category_id)
                    Status = "availible"
                    rooms = Room.objects.filter(Room_category=room_category.id, status=Status)
                    for r in rooms:
                        print(r.id)
                    message = []
                    for x_room in range(0, len(rooms)):
                        message.append({
                            'id': rooms[x_room].id,
                            'name': rooms[x_room].Room_NO,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "new_admission_form":
                if request.user.has_perm('APEN.add_admissionorder'):
                    # Get all data from the request
                    bed = request.POST.get('bed')
                    room = request.POST.get('room')
                    guardianName = request.POST.get('guardianName')
                    guardianrelation = request.POST.get('guardianrelation')
                    guardianMobileNo = request.POST.get('guardianMobileNo')
                    guardianAddress = request.POST.get('guardianAddress')
                    hidden_admission_order = request.POST.get('hidden_admission_order')
                    
                    # Validaet data
                    if bed == '' or bed == 'null' or bed is None or bed == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select bed',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if room == '' or room == 'null' or room is None or room == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please select room ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if guardianName == '' or guardianName == 'null' or guardianName is None or guardianName == 'undefined':
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Patient\'s Father Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if text_validation(guardianName) == False:
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if guardianrelation == '' or guardianrelation == 'null' or guardianrelation is None or guardianrelation == 'undefined':
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Patient\'s Father Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if text_validation(guardianrelation) == False:
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if guardianMobileNo == '' or guardianMobileNo == 'null' or guardianMobileNo is None or guardianMobileNo == 'undefined':
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Patient\'s Father Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if number_validation(guardianMobileNo) == False:
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if guardianAddress == '' or guardianAddress == 'null' or guardianAddress is None or guardianAddress == 'undefined':
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Enter Patient\'s Father Name',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if text_validationNumber(guardianAddress) == False:
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter text only',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    
                    

                    Status = "Active"
                    ad_order = AdmissionOrder.objects.get(id=hidden_admission_order)
                    room_id = Room.objects.get(id=room)
                    bed_id = Beds.objects.get(id=bed)
                    new_admission = Addmission(AddmissionNumber = GenerateAdmissionNumber() ,Admission_order_id = ad_order.id, GuardianName = guardianName, GuardianMobileNo = guardianMobileNo,  GuardianRelship= guardianrelation, GuardianAddress = guardianrelation, Status=Status)
                    new_admission.save()
                    current_admission = Addmission.objects.get(id = new_admission.id)
                    assign_bed = AssignBed(Bed_id = bed_id.id, Room_id = room_id.id, FromDate = current_admission.AddmissionDate, Admission_id = current_admission.id)
                    assign_bed.save()
                    # update bed
                    bed_id.status = "Occupied"
                    bed_id.save()
                    all_beds_full = Beds.objects.filter(Room=room_id, status='Occupied').count()
                    all_beds_in_room =room_id.beds_set.count()
                    if all_beds_in_room == all_beds_full:
                        room_id.status = 'full'
                        room_id.save()
                    else:
                        room_id.status = 'availible'
                        room_id.save()
                    ad_order.Status = "Approved"
                    ad_order.save()
                
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
                            'Message': 'You dont have permission to place admisson order',
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
def inpatient_list(request):
    try:
        if request.user.has_perm('APEN.view_addmission'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            DataNumber = 10
            SearchQuery = ''
            inpatient_list = []

            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])

            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                inpatient_list = Addmission.objects.filter(
                    Q(Patient__get_fullName__icontains=SearchQuery) |
                    Q(Doctor__first_name__icontains=SearchQuery)

                )
            else:
                inpatient_list = Addmission.objects.filter(Status="Active").order_by(
                        Case(
                            When(Admission_order__patient_priority="Emergency", then=1),
                            When(Admission_order__patient_priority="Urgent", then=2),
                            When(Admission_order__patient_priority="nonUrgent", then=3),
                            default=4,
                            output_field=models.IntegerField(),
                        )
                    )

            paginator = Paginator(inpatient_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {

                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Inpatient List',
            }
            return render(request, 'Patients/inpatient-list.html', context)
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
def inpatient_view_appointment(request, admission_id):
    try:
        if request.user.has_perm('APEN.view_addmission'):
            Admission = Addmission.objects.get(id=admission_id)
            patientFullName = Admission.Admission_order.Appointment.Patient.get_fullName
            patientgender = Admission.Admission_order.Appointment.Patient.PatientGender
            patientMobileNo = Admission.Admission_order.Appointment.Patient.PatientMobileNo
            patientAge = Admission.Admission_order.Appointment.Patient.PatientAge
            patientDistrict = Admission.Admission_order.Appointment.Patient.PatientDistrict
            patientVillage = Admission.Admission_order.Appointment.Patient.PatientVillage
            admission_id = admission_id
            examcategory = ExamCategory.objects.all()

            medicines = Medicine_categories.objects.all()

            operationCategory = OperationCategory.objects.all()

            medicine_prescription = MedicinesPrescription.objects.filter(Admission = admission_id, Status = "Approved")
            medications_for_dropdown = MedicinePrescriptionDetials.objects.filter(PrescriptionNo__in=[medicine_name.id for medicine_name in medicine_prescription])
            medications_list = MedicationDose.objects.filter(Admission=admission_id)

            nurses = Employee.objects.filter(job_type__name = "Nurse") # temporary filter

            Nurse_Notes = NurseNotes.objects.filter(Admission = admission_id)

            AssignedBed = AssignBed.objects.get(Admission = admission_id)

            try:
                Isdischarged = Discharge.objects.get(Admission = admission_id)
            except Discharge.DoesNotExist:
                Isdischarged = None




            # I'm gonna filter this code later by removing un-needed retrieves
                
            # passing for overview tab
            # for medicine prescriptions in overview
            Prescriped_medicines = MedicinesPrescription.objects.filter(Admission=admission_id)
            
            # for laboratory in overview
            ordered_laboratorities = LabTestOrders.objects.filter(Admission=admission_id)
            # for radiology in overview
            ordered_radiology = RadiologyOrders.objects.filter(Admission=admission_id)
            # for patient operation
            PatientOperation = Patient_operation.objects.filter(Admission=admission_id)


            # # passing fo diagnosis
            # # for laboratory in diagnosis tab
            # for ordered_lab in ordered_laboratorities:
            #     lab_order_details = LabTestOrderDetails.objects.filter(LabTestOrder=ordered_lab.id)
                

            medicines = pharmacy_medicine.objects.all()
            medicineCategories = Medicine_categories.objects.all()
            medicines = Medicine_categories.objects.all()
            medicineCategories = Medicine_categories.objects.all()
            labTests = LabTests.objects.all()
            radiologyExam = RadiologyExam.objects.all()
            examcategory = ExamCategory.objects.all()
            labgroups = LabTestGroups.objects.all()
            Status = "Approved"
            lab_order = LabTestOrders.objects.filter(Admission=admission_id)
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
                ordered_lab = LabTestOrders.objects.filter(Admission=admission_id)
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
                
            RadiologyOrder = RadiologyOrders.objects.filter(Admission=admission_id)
            ordered_radio=""
            radio_result_list=[]
            radiology_exams = [] # passing for View prescription
            radio_result_details_list = []
            if RadiologyOrder:
                ordered_radio = RadiologyOrders.objects.filter(Admission=admission_id)
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
            Prescriped_medicine = MedicinesPrescription.objects.filter(Admission=admission_id)
            for prescripe in Prescriped_medicine:
                prescriped_medicine_details = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=prescripe)
                for p in prescriped_medicine_details:
                    prescriped_medicine_details_list.append(p)
        
            
            # passing for operations
            Operation = Operations.objects.all()
            operationCategory = OperationCategory.objects.all()
            # I'm pasing all employees bcz jobtype is not ready yet so can't do filter
            Employees = Employee.objects.all()
            # for Patient's Operations Table
            PatientOperation = Patient_operation.objects.filter(Admission=admission_id)
        
                # for diagnosis view
            blood_properties = LabTest_Blood_Properties.objects.all()
            
            context = {
                'Admission':Admission,
                'patientFullName':patientFullName,
                'patientgender':patientgender,
                'patientMobileNo':patientMobileNo,
                'patientAge':patientAge,
                'patientDistrict':patientDistrict,
                'patientVillage':patientVillage,
                'admission_id':admission_id,
                'examcategory':examcategory,
                'Medicines':medicines,
                'OperationCategories': operationCategory,
                'medications_list':medications_for_dropdown,
                'medications':medications_list,
                'nurses':nurses,
                'Nurse_Notes':Nurse_Notes,
                'AssignedBed':AssignedBed,
                'Isdischarged':Isdischarged,

                # this code needs more filtering 

                
                # ----start passing for overview tab
                # for medicine prescriptions in overview
                'Prescriped_medicines': Prescriped_medicines,
                # for laboratory in overview
                'ordered_laboratorities': ordered_laboratorities,
                # for radiology in overview
                'ordered_radiology': ordered_radiology,
                # for patient operation in overview
                'PatientOperation': PatientOperation,
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
                'id': id,
                
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
                # passing for operations
                'Operations': Operation,
                'OperationCategories': operationCategory,
                'Employees': Employees,
                'PatientOperation': PatientOperation,
                
            
                
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
            return render(request, 'Patients/inpatient-view.html', context)
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
def inpatient_view_emergency(request, admission_id):
    try:
        if request.user.has_perm('APEN.view_addmission'):
            Admission = Addmission.objects.get(id=admission_id)
            patientFullName = Admission.Admission_order.Visit.Patient.get_fullName
            patientgender = Admission.Admission_order.Visit.Patient.PatientGender
            patientMobileNo = Admission.Admission_order.Visit.Patient.PatientMobileNo
            patientAge = Admission.Admission_order.Visit.Patient.PatientAge
            patientDistrict = Admission.Admission_order.Visit.Patient.PatientDistrict
            patientVillage = Admission.Admission_order.Visit.Patient.PatientVillage
            admission_id = admission_id
            medicines = Medicine_categories.objects.all()
            examcategory = ExamCategory.objects.all()
            operationCategory = OperationCategory.objects.all()
            medicine_prescription = MedicinesPrescription.objects.filter(Admission = admission_id, Status = "Approved")
            medications_for_dropdown = MedicinePrescriptionDetials.objects.filter(PrescriptionNo__in=[medicine_name.id for medicine_name in medicine_prescription])
            medications_list = MedicationDose.objects.filter(Admission=admission_id)
            nurses = Employee.objects.filter(job_type__name = "Nurse") # temporary filter

            Nurse_Notes = NurseNotes.objects.filter(Admission = admission_id)

            AssignedBed = AssignBed.objects.get(Admission = admission_id)
            try:
                Isdischarged = Discharge.objects.get(Admission = admission_id)

            except Discharge.DoesNotExist:
                Isdischarged = None


            # I'm gonna filter this code later by removing un-needed retrieves
                
            # passing for overview tab
            # for medicine prescriptions in overview
            Prescriped_medicines = MedicinesPrescription.objects.filter(Admission=admission_id)
            
            # for laboratory in overview
            ordered_laboratorities = LabTestOrders.objects.filter(Admission=admission_id)
            # for radiology in overview
            ordered_radiology = RadiologyOrders.objects.filter(Admission=admission_id)
            # for patient operation
            PatientOperation = Patient_operation.objects.filter(Admission=admission_id)


            # # passing fo diagnosis
            # # for laboratory in diagnosis tab
            # for ordered_lab in ordered_laboratorities:
            #     lab_order_details = LabTestOrderDetails.objects.filter(LabTestOrder=ordered_lab.id)
                

            medicines = pharmacy_medicine.objects.all()
            medicineCategories = Medicine_categories.objects.all()
            Appointment = Appointments.objects.get(id=admission_id)
            medicines = Medicine_categories.objects.all()
            medicineCategories = Medicine_categories.objects.all()
            labTests = LabTests.objects.all()
            radiologyExam = RadiologyExam.objects.all()
            examcategory = ExamCategory.objects.all()
            labgroups = LabTestGroups.objects.all()
            Status = "Approved"
            lab_order = LabTestOrders.objects.filter(Admission=admission_id)
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
                ordered_lab = LabTestOrders.objects.filter(Admission=admission_id)
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
                
            RadiologyOrder = RadiologyOrders.objects.filter(Admission=admission_id)
            ordered_radio=""
            radio_result_list=[]
            radiology_exams = [] # passing for View prescription
            radio_result_details_list = []
            if RadiologyOrder:
                ordered_radio = RadiologyOrders.objects.filter(Admission=admission_id)
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
            Prescriped_medicine = MedicinesPrescription.objects.filter(Admission=admission_id)
            for prescripe in Prescriped_medicine:
                prescriped_medicine_details = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=prescripe)
                for p in prescriped_medicine_details:
                    prescriped_medicine_details_list.append(p)
        
            
            # passing for operations
            Operation = Operations.objects.all()
            operationCategory = OperationCategory.objects.all()
            # I'm pasing all employees bcz jobtype is not ready yet so can't do filter
            Employees = Employee.objects.all()
            # for Patient's Operations Table
            PatientOperation = Patient_operation.objects.filter(Admission=admission_id)
            
        
        
            
            # for medicine prescription available quantity
            for l in unique_blood:
                print(l.TestID.id)
            print(lab_blood_list)
            # for diagnosis view
            blood_properties = LabTest_Blood_Properties.objects.all()
            context = {
                'Admission':Admission,
                'patientFullName':patientFullName,
                'patientgender':patientgender,
                'patientMobileNo':patientMobileNo,
                'patientAge':patientAge,
                'patientDistrict':patientDistrict,
                'patientVillage':patientVillage,
                'admission_id':admission_id,
                'Medicines':medicines,
                'examcategory':examcategory,
                'OperationCategories': operationCategory,
                'medications_list':medications_for_dropdown,
                'medications':medications_list,
                'nurses':nurses,
                'Nurse_Notes':Nurse_Notes,
                'AssignedBed':AssignedBed,
                'Isdischarged':Isdischarged,

                # this code needs more filtering 

                
                # ----start passing for overview tab
                # for medicine prescriptions in overview
                'Prescriped_medicines': Prescriped_medicines,
                # for laboratory in overview
                'ordered_laboratorities': ordered_laboratorities,
                # for radiology in overview
                'ordered_radiology': ordered_radiology,
                # for patient operation in overview
                'PatientOperation': PatientOperation,
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
                'Medicines': medicines,
                'MedicineCategories': medicineCategories,
                'id': id,
                
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
                'Appointment': Appointment,
                'Status': Status,
                # passing for operations
                'Operations': Operation,
                'OperationCategories': operationCategory,
                'Employees': Employees,
                'PatientOperation': PatientOperation,
                
            
                
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
            return render(request, 'Patients/inpatient-view.html', context)
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
                    # Get all data from the request
                    admission_id = request.POST.get('admission_id')
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
                        admission = Addmission.objects.get(id=admission_id)
                        Status = "Pending"
                        # save medicine prescription 
                        new_medicine_prescription = MedicinesPrescription(instructions = Instructions ,Admission_id = admission.id, PrescriptionNo=GeneratePrescriptionNumber(), Ordered_by = "Inpatient Unit", Status=Status)
                        new_medicine_prescription.save()
                        # save medicines prescription details using medicine prescription order ID
                        Current_medicine_prescription = MedicinesPrescription.objects.get(pk=new_medicine_prescription.id)
                        for (med, dose, dose_interval, dose_duration, quantity) in zip(medicine, Dose, DoseInterval, DoseDuration, Quantity):
                            med_id = Medicine.objects.get(id=med)
                            get_medicine = pharmacy_medicine.objects.get(Medicine_name_id=med_id.id)
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
                    medicine_transection_id = Medicine.objects.get(id=medicine_id)
                    medicine = pharmacy_medicine.objects.filter(
                        Medicine_name=medicine_transection_id.id)
                    print(medicine_id)
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
def manage_patient_diagnosis(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_diagnosis':
                if request.user.has_perm('APEN.add_labtestorders') or request.user.has_perm('APEN.add_radiologyorders'):
                    admission_id = request.POST.get('admission_id')
                    laboratory = request.POST.get('laboratory')
                    radiology = request.POST.get('radiology')
                    admission_id = Addmission.objects.get(id=admission_id)
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
                                
                            new_lab_order = LabTestOrders(Admission_id = admission_id.id,TestOrderNumber=GenerateTestOrderNumber(), Ordered_by = "Inpatient Unit", Status=Status)
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
                            new_radiology_order = RadiologyOrders(Admission_id = admission_id.id,RadiologyOrderNumber=GenerateRadiologyOrderNumber(), Ordered_by = "Inpatient Unit" ,Status=Status)
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
                    lab_category_list = []
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
def manage_patient_operation(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_patient_operation':
                if request.user.has_perm('APEN.add_patient_operation'):
                    # Get all data from the request
                    admission_id = request.POST.get('admission_id')
                    Operation = request.POST.get('Operation')
                    OperationCategory = request.POST.get('OperationCategory')
                    OperationDate = request.POST.get('OperationDate')
                
                    if Operation == '' or Operation == 'null' or Operation is None or Operation == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Select Operation name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if OperationCategory == '' or OperationCategory == 'null' or OperationCategory is None or OperationCategory == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Select OperationCategory ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                        
                    if OperationDate == '' or OperationDate == 'null' or OperationDate is None or OperationDate == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter OperationDate ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
            
                    admission_id = Addmission.objects.get(id=admission_id)
                
                    Operation_id = Operations.objects.get(id=Operation)
                   
                    new_operation = Patient_operation(Admission_id = admission_id.id, Operation= Operation_id, OperationDate = OperationDate, Status= "Pending")
                    new_operation.save()
                
                    return JsonResponse(
                                {
                                    'isError': False,
                                    'Message': 'new Patient Operation has been created',
                                    'title': 'masha allah !',
                                    'type': 'success+',
                                }
                            ) 
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to Add an Operation for patient',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )
            if action == "get_category_operation":
                if request.user.has_perm('APEN.add_patient_operation'):
                    operation_id = request.POST.get('operationCategory')
                    get_operation_id = Operations.objects.filter(
                        CategoryName=operation_id)
                    # get_dep_section = Sections.objects.filter(departments = depart_id)
                    # base_pay = 0

                    message = []
                    for xoperations in range(0, len(get_operation_id)):

                        message.append({
                            'id': get_operation_id[xoperations].id,
                            'name': get_operation_id[xoperations].OperationName,
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
def manage_patient_profile(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_medicine_dose':
                if request.user.has_perm('APEN.add_medicationdose'):

                    # Get all data from the request
                    admission_id = request.POST.get('admission_id')

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
                    admission_id = Addmission.objects.get(id=admission_id)
                    new_medicine_dose = MedicationDose(Admission_id = admission_id.id, Medication_date=MedicationsDose_date, Medicition_time=MedicationsDose_time, Medication_name=medicine_name, Medication_dose=Medication_dose, Medicition_Remarks=Remarks) 
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
            
            if action == 'new_NurseNotes':
                if request.user.has_perm('APEN.add_nursenotes'):

                    # Get all data from the request
                    admission_id = request.POST.get('admission_id')
                    note_dateTime = request.POST.get('note_dateTime')
                    Nurse = request.POST.get('Nurse')
                    Note = request.POST.get('Note')
                    Comment = request.POST.get('Comment')
                    

                    if note_dateTime == '' or note_dateTime == 'null' or note_dateTime is None or note_dateTime == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Note Date Time',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if Nurse == '' or Nurse == 'null' or Nurse is None or Nurse == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Select Nurse Name',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                
                    if Note == '' or Note == 'null' or Note is None or Note == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please Enter Note',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    
                    if text_validationNumber(Note) == False:
                                return JsonResponse(
                                    {
                                        'isError': True,
                                        'Message': 'Please enter valid text for Note',
                                        'title': 'Validation Error!',
                                        'type': 'warning',
                                    }
                                )
                
                    if Comment != '':
                        if text_validationNumber(Comment) == False:
                                    return JsonResponse(
                                        {
                                            'isError': True,
                                            'Message': 'Please enter valid text for Comment',
                                            'title': 'Validation Error!',
                                            'type': 'warning',
                                        }
                                    )
                    Note = RemoveSpecialCharacters(Note)
                    Comment = RemoveSpecialCharacters(Comment)
                    addmission_id = Addmission.objects.get(id = admission_id)
                    nurse_id = Employee.objects.get(id=Nurse)
                    new_nurseNotes = NurseNotes(Admission_id=addmission_id.id, Note_dateTime=note_dateTime, Nurse_id=nurse_id.id, Note=Note, Comment=Comment) 
                    new_nurseNotes.save()
                
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
                            'Message': 'New Nurse Note has been added',
                            'title': 'Masha Allah !',
                            'type': 'success+',
                        }
                    )      
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to add Nurse Notes',
                            'title': 'Access is Denied !',
                            'type': 'warning',

                        },
                    )             

            if action == 'new_discharge':
                if request.user.has_perm('APEN.add_discharge'):

                    # Get all data from the request
                    
                    admission_id = request.POST.get('admission_id')

                    discharge_date = request.POST.get('discharge_date')
                    dischargeStatus = request.POST.get('dischargeStatus')


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

                    diagnosis_result = RemoveSpecialCharacters(diagnosis_result)
                    surgery_operations = RemoveSpecialCharacters(surgery_operations)
                    discharge_note = RemoveSpecialCharacters(discharge_note)
                    death_reason = RemoveSpecialCharacters(death_reason)
                    referel_reason = RemoveSpecialCharacters(referel_reason)

                    admission = Addmission.objects.get(id=admission_id)
                
                    if dischargeStatus == "Referrel":
                        new_referel_patient = Referrel(HospitalName = hospital_name, Referel_Date=referel_date, Referel_Reason=referel_reason)
                        new_referel_patient.save()
                        current_referel = Referrel.objects.get(id=new_referel_patient.id)
                        new_dischagre_referel = Discharge(Admission_id=admission.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result, referrel_id= current_referel.id) 
                        new_dischagre_referel.save()
                    elif dischargeStatus == "Normal":
                        new_dischagre_normal = Discharge(Admission_id=admission.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result) 
                        new_dischagre_normal.save()
                    elif dischargeStatus == "Death":  
                        new_death_patient = PatientDeath(Death_Date = death_date, Death_Reason=death_reason)
                        new_death_patient.save()
                        current_death = PatientDeath.objects.get(id=new_death_patient.id)
                        new_dischagre_death = Discharge(Admission_id=admission.id, dischargeStatus=dischargeStatus, Operation=surgery_operations, Note=discharge_note, Diagnosis=diagnosis_result, death_id= current_death.id) 
                        new_dischagre_death.save()
                
                    else:
                        return render(request, 'Hr/404.html')
                    
                    try:
                        assigned_bed = AssignBed.objects.get(Admission_id=admission.id,)
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
                

                    admission.DischargeDate = discharge_date
                    admission.Status = "Discharged"
                    admission.save()

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
                            'Message': 'You dont have permission to Discharge a Patient',
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
def discharged_inpatients_list(request):
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
               discharged_list = Discharge.objects.filter(Admission_id__isnull=False, **dataFiltering)

            paginator = Paginator(discharged_list, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
        
                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Dishcarged InPatient List',
                'discharge_status':dischrge_status,
            }
            return render(request, 'Patients/discharged_inpatients.html', context)
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
    

def GenerateAdmissionNumber():
    try:
        last_id = Addmission.objects.filter(~Q(AddmissionNumber=None)).last()
        serial = 0
        today = datetime.today().strftime('%d/%m/%y')
        today_without_slashes = today.replace('/', '')
        if last_id is not None:
            serial = int(last_id.AddmissionNumber[8:])
        serial = serial + 1

        if serial < 10:
            serial = '000' + str(serial)
        elif serial < 100:
            serial = '00' + str(serial)
        elif serial < 1000:
            serial = '0' + str(serial)

        return f"AD{today_without_slashes}{serial}"
    except Exception as error:
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)
 