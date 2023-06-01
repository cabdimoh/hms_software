from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

from LRPD.LabResult import GenerateTestOrderNumber
from LRPD.radiology import GenerateRadiologyOrderNumber
from .models import *
from Hr.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from Inventory.models import *
from LRPD.models import *
from Users.models import Users
from Users.models import sendException
from Users.views import sendTrials
currentDate = date.today()
from Hr.views import RemoveSpecialCharacters, text_validation, text_validationNumber,  number_validation, phone_valid, check
# Create your views here.
currentDate = date.today()
# ------------------Patients---------------------------
@login_required(login_url='Login')
def outpatient_list(request):
    try:
        if request.user.has_perm('APEN.view_patients'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            CheckDate = 'dataDate' in request.GET
            dataDate = currentDate.strftime('%Y-%m-%d')
            DataNumber = 10
            SearchQuery = ''
            AppointmentList = []
            Status="Approved"
            if CheckDate:
                dataDate = request.GET['dataDate']
                expand = [int(x) for x in dataDate.split('-')]
                dataDate = date(expand[0] , expand[1] , expand[2]).strftime('%Y-%m-%d')
            if CheckDataNumber:
                DataNumber = int(request.GET['DataNumber'])
            if CheckSearchQuery:
                SearchQuery = request.GET['SearchQuery']
                if request.user.is_staff:
                    AppointmentList = Appointments.objects.filter(
                        Q(Status__icontains=Status) &
                        (
                        Q(Patient__PatientFirstName__icontains=SearchQuery) |
                        Q(Patient__PatientLastName__icontains=SearchQuery) |
                        Q(Patient__PatientFirstName__icontains=SearchQuery) & Q(Patient__PatientLastName__icontains=SearchQuery) & Q(Patient__PatientMiddleName__icontains=SearchQuery)|
                        Q(AppointmentNumber__icontains=SearchQuery) |
                        Q(Doctor__first_name__icontains=SearchQuery) |
                        Q(jobtypes__name__icontains=SearchQuery) |
                        Q(AppointmentDate__icontains=SearchQuery)),AppointmentDate=dataDate
                    )
                else:
                        AppointmentList = Appointments.objects.filter(
                       Q(Status__icontains=Status) &
                        (Q(Patient__PatientFirstName__icontains=SearchQuery) |
                        Q(Patient__PatientLastName__icontains=SearchQuery) |
                        Q(Patient__PatientFirstName__icontains=SearchQuery) & Q(Patient__PatientLastName__icontains=SearchQuery) & Q(Patient__PatientMiddleName__icontains=SearchQuery)|
                        Q(AppointmentNumber__icontains=SearchQuery) |
                        Q(Doctor__first_name__icontains=SearchQuery) |  
                        Q(jobtypes__name__icontains=SearchQuery) |

                        Q(AppointmentDate__icontains=SearchQuery)),AppointmentDate=dataDate
                    )
            else:
                if request.user.is_superuser:
                    AppointmentList = Appointments.objects.filter(
                        Q(AppointmentDate__icontains=dataDate) &
                        Q(Status__icontains=Status) 
                    )
                else:
                    AppointmentList = Appointments.objects.filter(
                        Q(AppointmentDate__icontains=dataDate) &
                        Q(Status__icontains=Status) & Q(Doctor=request.user.employee)
                    )
                     # If the appointment list is empty, try again without the doctor condition
                    if not AppointmentList:  
                        AppointmentList = Appointments.objects.filter(
                            Q(AppointmentDate__icontains=dataDate) &
                            Q(Status__icontains=Status)
                        )
            paginator = Paginator(AppointmentList, DataNumber)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            Speciality = Title.objects.all()
            Doctor = Employee.objects.all()
            context = {
                'Specialities': Speciality,
                'Doctors': Doctor,
                'page_objects': page_obj,
                'SearchQuery': SearchQuery,
                'DataNumber': DataNumber,
                'pageTitle': 'Appointment List',
                'dataDate': dataDate,   
            }
            return render(request, 'Patients/patient-list.html', context)
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
def patient_view(request, id):
    try:
        if request.user.has_perm('APEN.view_patients'):
            Appointment = Appointments.objects.get(id=id)
            unique_categories = []
            # passing for overview tab
            # for medicine prescriptions in overview
            Prescriped_medicines = MedicinesPrescription.objects.filter(Appointment=id)
            for prescriped_medicine in Prescriped_medicines:
                unique_categories = Medicine_categories.objects.filter(
                    id__in=[pm.MedicineName.Medicine_categories.id for pm in prescriped_medicine.medicineprescriptiondetials_set.all()]
                )            
            
            # for laboratory in overview
            ordered_laboratorities = LabTestOrders.objects.filter(Appointment=id)
            # for radiology in overview
            ordered_radiology = RadiologyOrders.objects.filter(Appointment=id)
            # for patient operation
            PatientOperation = Patient_operation.objects.filter(Appointment=id)
                
            medicines = pharmacy_medicine.objects.all()
            pharmacy_med_category = Medicine_categories.objects.filter(id__in=[med.Medicine_categories.id for med in medicines])

            Appointment = Appointments.objects.get(id=id)
            labTests = LabTests.objects.all()
            radiologyExam = RadiologyExam.objects.all()
            examcategory = ExamCategory.objects.all()
            labgroups = LabTestGroups.objects.all()
            Status = "Approved"
            lab_order = LabTestOrders.objects.filter(Appointment=id)
            ordered_lab=""

            test_group_list =[]
            test_subgroup_list =[]
            unique_parameter_result =[]
            unique_types_list =[]
            lab_parameter_list = []
            lab_blood_list = []
            lab_result_list = []
            radio_result_list = []
            prescriped_medicine_details_list = []
            lab_tests_list = []
            lab_blood_result_list = []
            lab_parameter_result_list = []
            unique_blood = []
            unique_group_list = []
            unique_subgroup_list = []
            unique_result_parameter_list = []
            radio_result_details_list = []
            radiology_exams = []
            if lab_order:
                ordered_lab = LabTestOrders.objects.filter(Appointment=id)
                for lab in ordered_lab:
                    lab_result_list = LabTestResult.objects.filter(LabTestOrder_id=lab.id)
                    for laboratory_result in lab_result_list:
                        lab_blood_result_list = Lab_Blood_Results.objects.filter(labTest_result=laboratory_result.id)
                        for lab_blood_result in lab_blood_result_list:

                            test_groups = LabTestGroups.objects.filter(id=lab_blood_result.TestID.Group.id)
                            for unique in test_groups:
                                test_group_list.append(unique.id)
                            test_subgroups = LabTestSubGroups.objects.filter(id=lab_blood_result.TestID.SubGroup.id)
                            for unique in test_subgroups:
                                test_subgroup_list.append(unique.id)
                        lab_parameter_result_list = Lab_ExaminationParameters_Results.objects.filter(labTest_result=laboratory_result.id)
                        for lab_parameter_result in lab_parameter_result_list:
                            unique_parameter_result.append(lab_parameter_result.TestID.id)
                            unique_types_list.append(lab_parameter_result.Parameter.Type)
                    lab_tests_list = LabTestOrderDetails.objects.filter(LabTestOrder=lab.id)
                    for lab_test in lab_tests_list:
                        lab_blood_list = LabTest_Blood_Properties.objects.filter(TestID = lab_test.Test.id)
                       
                        lab_parameter_list = LabExaminationParameters.objects.filter(Test_id = lab_test.Test.id)
                         
            # for view lab 
            unique_parameter = set(lab_parameter_list)
            for u in unique_parameter:
                unique_parameter_list = LabExaminationParameters.objects.filter(Test_id=u)
            unique_result_parameter = set(unique_parameter_result)
            for u in unique_result_parameter:
                unique_result_parameter_list = LabTests.objects.filter(id=u)
                
            unique_groups = set(test_group_list)
            for unique in unique_groups:
                unique_group_list = LabTestGroups.objects.filter(id=unique)
               
            unique_subgroups = set(test_subgroup_list)
            for unique in unique_subgroups:
                unique_subgroup_list = LabTestSubGroups.objects.filter(id=unique)
                
            unique_types = set(unique_types_list)
            
              
            set_unique_lab_blood = set(lab_blood_list)
            for unique in set_unique_lab_blood:
                unique_blood = LabTest_Blood_Properties.objects.filter(id=unique)
                
                
            RadiologyOrder = RadiologyOrders.objects.filter(Appointment=id)
            ordered_radio=""

            if RadiologyOrder:
                ordered_radio = RadiologyOrders.objects.filter(Appointment=id)
                for radio in ordered_radio:
                    radio_result_list = RadiologyResult.objects.filter(RadiologyOrder_id=radio.id)
                    for radiology_result in radio_result_list:
                        radio_result_details_list = RadiologyResultDetails.objects.filter(Radiology_Result=radiology_result.id)
                    radiology_exams = RadiologyOrderDetails.objects.filter(RadiologyOrder=radio.id)
                  
            
            #for prescriptions
            Prescriped_medicine = MedicinesPrescription.objects.filter(Appointment=id)
            for prescripe in Prescriped_medicine:
                prescriped_medicine_details_list = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=prescripe)
                
        
            
            # passing for operations
            Operation = Operations.objects.all()
            operationCategory = OperationCategory.objects.all()
            # I'm pasing all employees bcz jobtype is not ready yet so can't do filter
            Employees = Employee.objects.all()
            # for Patient's Operations Table
            PatientOperation = Patient_operation.objects.filter(Appointment=id)
            
            # for treatement history
            treatementList = Appointments.objects.exclude(id=id).filter(Patient=Appointment.Patient.id)
           
            
        
            # for diagnosis view
            blood_properties = LabTest_Blood_Properties.objects.all()
           
            context = {
                'id': id,
                'Appointment': Appointment,
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
                'MedicineCategories': unique_categories,
                'pharmacy_med_category': pharmacy_med_category,
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
                
                #passing for treatment history
                'treatementHistory': treatementList,
              
                
                #passing for prescriped medicine
                'Prescriped_medicine_details': prescriped_medicine_details_list,
                'Prescriped_medicine':Prescriped_medicine,
                
                #passing for view lab tests and results
                'ordered_lab_tests_list':lab_tests_list,
                'lab_blood_result_list':lab_blood_result_list,
                'lab_parameter_result_list':lab_parameter_result_list,
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
          
            return render(request, 'Patients/Patient-View.html', context)
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
                    appointment_id = request.POST.get('appointmentId')
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

                        appointmentId = Appointments.objects.get(id=appointment_id)
                        if appointmentId.Status == "Pending":
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
                            new_medicine_prescription = MedicinesPrescription(instructions = Instructions ,Appointment_id=appointmentId.id, PrescriptionNo=GeneratePrescriptionNumber(), Ordered_by = "Outpatient Unit", Status=Status)
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
                    print(medicine_id)
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
            if action == "get_treatementHistory":
                if request.user.has_perm('APEN.add_medicinesprescription'):
                    id = request.POST.get('appointment_id')
                    appointment = Appointments.objects.get(id=id)
                    lab_order = LabTestOrders.objects.filter(Appointment=id)
                    ordered_lab=""
                    lab_result_list=[]
                    if lab_order:
                        ordered_lab = LabTestOrders.objects.filter(Appointment=id)
                        for lab in ordered_lab:
                            lab_result = LabTestResult.objects.filter(LabTestOrder_id=lab.id)
                            for laboratory_result in lab_result:
                                lab_result_list.append(laboratory_result)
                            
                        
                    RadiologyOrder = RadiologyOrders.objects.filter(Appointment=id)
                    ordered_radio=""
                    radio_result_list=[]
                    if RadiologyOrder:
                        ordered_radio = RadiologyOrders.objects.filter(Appointment=id)
                        for radio in ordered_radio:
                            radio_result = RadiologyResult.objects.filter(RadiologyOrder_id=radio.id)
                            for radiology_result in radio_result:
                                radio_result_list.append(radiology_result)
                        
                    
                    
                    #for prescriptions
                    prescriped_medicine_details_list =[]
                    Prescriped_medicine = MedicinesPrescription.objects.filter(Appointment=id)
                    for prescripe in Prescriped_medicine:
                        prescriped_medicine_details = MedicinePrescriptionDetials.objects.filter(PrescriptionNo=prescripe)
                        for p in prescriped_medicine_details:
                            prescriped_medicine_details_list.append(p)
                    message = {
                        'appointmentId': appointment.id,
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
def manage_patient_diagnosis(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_diagnosis':
                if request.user.has_perm('APEN.add_labtestorders') or request.user.has_perm('APEN.add_radiologyorders'):
                    appointment_id = request.POST.get('appointmentId')
                    laboratory = request.POST.get('laboratory')
                    radiology = request.POST.get('radiology')
                    appointmentId = Appointments.objects.get(id=appointment_id)
                    Status = "Pending"
                    if laboratory or radiology:
                        if appointmentId.Status == "Pending":
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please first approve patient before you prescribe Diagnosis',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                        else:
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
                                
                                new_lab_order = LabTestOrders(Appointment_id=appointmentId.id,TestOrderNumber=GenerateTestOrderNumber(), Ordered_by = "Outpatient Unit" , Status=Status)
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
                                new_radiology_order = RadiologyOrders(Appointment_id=appointmentId.id,RadiologyOrderNumber=GenerateRadiologyOrderNumber(), Ordered_by = "Outpatient Unit" ,Status=Status)
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
                    print(sample)
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
                    print(group_id)
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
            if action == "view_lab_order":
                if request.user.has_perm('APEN.view_labtestorders'):
                    clicked_order = request.POST.get('clicked_order')
                    has_blood_tests = None
                    has_urine_tests = None
                    has_stool_tests = None
                    lab_order_result = LabTestResult.objects.get(LabTestOrder_id=clicked_order)
                    lab_blood_details = Lab_Blood_Results.objects.filter(labTest_result_id=lab_order_result.id)
                    if lab_blood_details:
                        
                        has_blood_tests =  True
                    else : 
                        has_blood_tests = False
                    lab_parameter_details = Lab_ExaminationParameters_Results.objects.filter(labTest_result_id = lab_order_result.id)
                    if lab_parameter_details:
                        for l_details in lab_parameter_details:
                            if l_details:
                                if l_details.TestID.SampleType == "Urine":
                                    has_urine_tests = True
                                    break
                                else: 
                                    has_urine_tests = False
                    else: 
                        has_urine_tests = False
                    lab_parameter_details = Lab_ExaminationParameters_Results.objects.filter(labTest_result_id = lab_order_result.id)
                    if lab_parameter_details:

                        for s_details in lab_parameter_details:
                            if s_details:
                                if s_details.TestID.SampleType == "Stool":
                                    has_stool_tests = True
                                    break
                                else:
                                    has_stool_tests = False
                    else:
                        has_stool_tests = False
                    print(has_blood_tests, 'b')
                    print(has_urine_tests, 'u')
                    print(has_stool_tests, 's')
                    message={
                        'has_blood_tests':has_blood_tests,
                        'has_urine_tests':has_urine_tests,
                        'has_stool_tests':has_stool_tests,
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render(request, 'Hr/404.html')
            if action == "get_lab_order_info":
                if request.user.has_perm('APEN.view_labtestorders'):
                    ordered_id = request.POST.get('order_id')
                    order = LabTestOrders.objects.get(id=ordered_id)
                    order_status = order.Status
                    pending_order_details = []
                    approved_order_details = []
                    group = ''
                    if order.Status == "Pending":
                        lab_order_details = LabTestOrderDetails.objects.filter(LabTestOrder = order.id)
                        for order_details in lab_order_details:
                            blood_properties = order_details.Test.get_blood_properties()
                            if blood_properties:
                                lab_group = LabTestGroups.objects.get(id=blood_properties['Group'])
                                group = lab_group.GroupName
                            else:
                                group = 'null'
                            testName = order_details.Test.TestName

                            # parameter_properties = order_details.Test.get_parameters_properties()
                            # if 
                            pending_order_details.append({
                                'testNumber': order_details.Test.TestNumber,
                                'sampleType': order_details.Test.SampleType,
                                'testName': testName,
                                'group': group,
                                'order_status': order_status,
                            })
                             

                    elif order.Status == "Approved":

                        lab_result = LabTestResult.objects.get(LabTestOrder = order.id)
                        unique_groups = None
                        unique_subgroups = None
                        try:
                            lab_blood_results = Lab_Blood_Results.objects.filter(labTest_result = lab_result.id)
                            if lab_blood_results:
                                for lab_blood_r in lab_blood_results:
                                    
                                    Group = LabTestGroups.objects.filter(id = lab_blood_r.TestID.Group.id)
                                    unique_groups = set(group.GroupName for group in Group)
                                    groups_list = [group for group in unique_groups]
                                    subGroup = LabTestSubGroups.objects.filter(id = lab_blood_r.TestID.SubGroup.id) 
                                    unique_subgroups = set(g.SubGroupName for g in subGroup)
                                    subgroups_list = [subgroup for subgroup in unique_subgroups]
                                    approved_order_details.append({
                                        'testNumber': lab_blood_r.TestID.TestID.TestNumber,
                                        'sampleType': lab_blood_r.TestID.TestID.SampleType,
                                        'testName':lab_blood_r.TestID.TestID.TestName,
                                        'resultValue':lab_blood_r.ResultValue,
                                        'flag':lab_blood_r.flag,
                                        'normalRange':lab_blood_r.TestID.NormalRange,
                                        'testUnit':lab_blood_r.TestID.TestUnit,
                                        'subGroup': subgroups_list,
                                        'Group': groups_list,
                                        'order_status': order_status,
                                    })
                            else:
                                approved_order_details.append({
                                        'blood_result': 'empty',
                                        'order_status': order_status,

                                    })
                            
                        except Lab_Blood_Results.DoesNotExist:
                            lab_blood_results = None
                        try:
                            types_list = None
                            lab_param_results = Lab_ExaminationParameters_Results.objects.filter(labTest_result = lab_result.id)
                            if lab_param_results:
                                for lab_parameter in lab_param_results:
                                    types = LabExaminationParameters.objects.filter(id = lab_parameter.Parameter.id)
                                    unique_types = set(t.Type for t in types)
                                    types_list = [type for type in unique_types]
                            print(types_list)
                        except Lab_ExaminationParameters_Results.DoesNotExist:
                            lab_param_results = None
                    message = {
                        'pending_order_details' : pending_order_details,
                        'approved_order_details' : approved_order_details,
                        'Comment': lab_result.Comment,

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
def manage_patient_operation(request, action):
    try:
        if request.method == 'POST':
            if action == 'new_patient_operation':
                if request.user.has_perm('APEN.add_patient_operation'):
                    # Get all data from the request
                    Appointment = request.POST.get('appointmentId')
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
                
                    Appointment_id = Appointments.objects.get(id=Appointment)
                    if Appointment_id.Status == "Pending":
                                return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please first approve patient before you order operation',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                                )
                    else:

                        Operation_id = Operations.objects.get(id=Operation)

                        new_operation = Patient_operation(Appointment = Appointment_id, Operation= Operation_id, OperationDate = OperationDate)
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
def order_admission(request, action):
    try:
        if action == "new_order_admission":
            if request.method == 'POST':
                if request.user.has_perm('APEN.add_admissionorder'):
                    # Get all data from the request
                    appointemntId = request.POST.get('appointmentId')
                    admission_date = request.POST.get('admission_date')
                    bedType = request.POST.get('bedType')
                    admission_reason = request.POST.get('admission_reason')
                    admission_note = request.POST.get('admission_note')
                    Patient_priority = request.POST.get('patient_priority')
                    
                    # Validaet data
                    if admission_date == '' or admission_date == 'null' or admission_date is None or admission_date == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter admission date',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )

                    if admission_reason == '' or admission_reason == 'null' or admission_reason is None or admission_reason == 'undefined':
                        return JsonResponse(
                            {
                                'isError': True,
                                'Message': 'Please enter admission reason ',
                                'title': 'Validation Error!',
                                'type': 'warning',
                            }
                        )
                    if text_validationNumber(admission_reason) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for Admission Reason',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    if admission_note != '' :
                        if text_validationNumber(admission_note) == False:
                            return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please enter valid text for Admission Note',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        admission_note = 'None'
                    get_appointment = Appointments.objects.get(id=appointemntId)
                    if get_appointment.Status == "Pending":
                        return JsonResponse(
                                {
                                    'isError': True,
                                    'Message': 'Please Accept the patient before Admitting',
                                    'title': 'Validation Error!',
                                    'type': 'warning',
                                }
                            )
                    else:
                        new_order = AdmissionOrder(Appointment_id = get_appointment.id, Ordered_by = "Outpatient Unit", AdmissionDate= admission_date, AdmissionReason=admission_reason, BedType=bedType, Status="Pending", Note=admission_note, patient_priority=Patient_priority )
                        new_order.save()
                        get_appointment.Status = "Admitted"
                        get_appointment.save()
                        return JsonResponse(
                                    {
                                        'isError': False,
                                        'Message': 'new Admission has been ordered',
                                        'title': 'masha allah !',
                                        'type': 'success+',
                                    }
                                ) 
                else:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to order an Admission',
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

def GeneratePrescriptionNumber():
    try:
        last_id = MedicinesPrescription.objects.filter(~Q(PrescriptionNo=None)).last()
        serial = 0
        today = datetime.today().strftime('%d/%m/%y')
        today_without_slashes = today.replace('/', '')
        if last_id is not None:
            serial = int(last_id.PrescriptionNo[9:])
        serial = serial + 1

        if serial < 10:
            serial = '000' + str(serial)
        elif serial < 100:
            serial = '00' + str(serial)
        elif serial < 1000:
            serial = '0' + str(serial)

        return f"P{today_without_slashes}{serial}"
    except Exception as error:
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)