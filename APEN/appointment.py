from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
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

@login_required(login_url='Login')
def appointment_list(request):
    try:
        if request.user.has_perm('APEN.view_appointments'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            CheckDate = 'dataDate' in request.GET
            dataDate = currentDate.strftime('%Y-%m-%d')
            DataNumber = 10
            SearchQuery = ''
            AppointmentList = []
            Status="Pending"
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
            return render(request, 'Appointments/appointment-list.html', context)
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
def cancelled_appointment_list(request):
    try:
        if request.user.has_perm('APEN.view_appointments'):
            CheckSearchQuery = 'SearchQuery' in request.GET
            CheckDataNumber = 'DataNumber' in request.GET
            CheckDate = 'dataDate' in request.GET
            dataDate = currentDate.strftime('%Y-%m-%d')
            DataNumber = 10
            SearchQuery = ''
            AppointmentList = []
            Status="Cancelled"
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
                        (Q(Patient__PatientFirstName__icontains=SearchQuery) |
                        Q(Doctor__first_name__icontains=SearchQuery) |
                        Q(AppointmentDate__icontains=SearchQuery)),AppointmentDate=dataDate
                    )
                else:
                        AppointmentList = Appointments.objects.filter(
                        Q(Status__icontains=Status) &
                        (Q(Patient__PatientFirstName__icontains=SearchQuery) |
                        Q(Doctor__first_name__icontains=SearchQuery) |
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
                'Status':Status,
            }
            return render(request, 'Appointments/appointment-list.html', context)
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
def add_appointments(request):
    try:
        if request.user.has_perm('APEN.add_appointments'):
            title_doctor = Title.objects.filter(name__icontains="Doctor")
            doctorList =[]
            for j in title_doctor:
                Doctor = Employee.objects.filter(job_type=j.id)
                for doc in Doctor:
                    doctorList.append(doc)
            Patient = Patients.objects.all()
            districts = ['Dharkenley', 'Deynile', 'HowlWadaag', 'Wardhigley', 'Waaberi', 'HamarJajab', 'Bondhere', 'Karaan',
                        'Yaaqshid', 'Huriwaa', 'Kaxda', 'Hodan', 'Shibis', 'Abdiaziz', 'Shangani', 'Wadajir', 'HamarWeyne']
            Gender = ['Male', 'Female']
            context = {
                
                'Doctors': doctorList,
                'Patients': Patient,
                'districts': districts,
                'Genders': Gender,
            }
            return render(request, 'Appointments/Add-Appointments.html', context)
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
def manage_appointment(request, action):
    try:       
        if action == 'new_appointment':
            if request.user.has_perm('APEN.add_appointments'):
                # Get all data from the request
                PatientFirstName = request.POST.get('PatientFirstName')
                PatientMiddleName = request.POST.get('PatientMiddleName')
                PatientLastName = request.POST.get('PatientLastName')
                PatientAge = request.POST.get('PatientAge')
                PatientVillage = request.POST.get('PatientVillage')
                jobtype_ids = request.POST.get('jobtype_ids')
                AppointmentDate = request.POST.get('AppointmentDate')
                PatientGender = request.POST.get('PatientGender')
                PatientMobileNo = request.POST.get('PatientMobileNo')
                PatientDistrict = request.POST.get('PatientDistrict')
                PatientMarital = request.POST.get('PatientMarital')
                
                Doctor = request.POST.get('Doctor')
                hidden_btn = request.POST.get('hidden_btn')

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
                            'Message': 'Please enter text only for patient father name',
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
                            'Message': 'Please enter text only for patient last name',
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
                            'Message': 'Please enter nums only for patient age',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientVillage == '' or PatientVillage == 'null' or PatientVillage is None or PatientVillage == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Patient Village',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if text_validationNumber(PatientVillage) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter valid text for patient village',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if jobtype_ids == '' or jobtype_ids == 'null' or jobtype_ids is None or jobtype_ids == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select a Specialityt',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if AppointmentDate == '' or AppointmentDate == 'null' or AppointmentDate is None or AppointmentDate == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select an Appointment Date',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientMobileNo == '' or PatientMobileNo == 'null' or PatientMobileNo is None or PatientMobileNo == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Patient\'s Mobile Number',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if number_validation(PatientMobileNo) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter numbers only for patient mobile number',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientDistrict == '' or PatientDistrict == 'null' or PatientDistrict is None or PatientDistrict == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select Patient\'s District',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientMarital == '' or PatientMarital == 'null' or PatientMarital is None or PatientMarital == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select Patient Maritial Status',
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
                if Doctor == '' or Doctor == 'null' or Doctor is None or Doctor == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select a doctor',
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
                Status = "Pending"
                Receptionist = Users.objects.get(id=request.user.id)
                if hidden_btn:
                    get_existing_patient = Patients.objects.get(id=hidden_btn)
                    New_Appointment_existing_patient = Appointments(AppointmentDate=AppointmentDate, AppointmentNumber=GenerateAppointmentNumber(), Doctor_id=Doctor, Patient_id=get_existing_patient.id, jobtypes_id=jobtype_ids, Status=Status, Receptionist=Receptionist)
                    New_Appointment_existing_patient.save()
                else:
                    pattfullname = PatientFirstName +' '+ PatientMiddleName +' '+ PatientLastName
                    New_Patient = Patients(PatientFirstName=PatientFirstName, PatientMiddleName=PatientMiddleName, PatientLastName=PatientLastName, PatientAge=PatientAge, PatientVillage=PatientVillage,
                                        PatientGender=PatientGender, PatientMobileNo=PatientMobileNo, PatientDistrict=PatientDistrict, PatientMaritalStatus=PatientMarital)
                    New_Patient.save()
                    Current_Patient = Patients.objects.get(pk=New_Patient.id)
                    New_Appointment = Appointments(AppointmentDate=AppointmentDate,AppointmentNumber=GenerateAppointmentNumber(), Doctor_id=Doctor, Patient_id=Current_Patient.id, jobtypes_id = jobtype_ids, Status=Status, Receptionist=Receptionist)
                    New_Appointment.save()
                    username = request.user.username
                    names = request.user.first_name + ' ' + request.user.last_name
                    avatar = str(request.user.avatar)
                    module = "Patient/ Appointment module"
                    action = f'{names} ayaa diwaan geliye Bukaan cusub oo magaciisu yahay {PatientFirstName} {PatientMiddleName}  {PatientLastName}'
                    path = request.path
                    sendTrials(request, username, names,
                            avatar, action, module, path)

                return JsonResponse(
                    {
                        'isError': False,
                        'Message': 'New Appointment has been created',
                        'title': 'Masha Allah !',
                        'type': 'success',
                    }
                    )
            else:
                return JsonResponse(
                    {
                        'isError': True,
                        'Message': 'You dont have permission to Add an Appointment',
                        'title': 'Access is Denied !',
                        'type': 'warning',

                    },
                )

        if action == "getAppointmentData":
            if request.user.has_perm('APEN.add_appointments'):
                id = request.POST.get('AppointmentId')

                is_exist = Appointments.objects.filter(id=id).exists()

                if is_exist:
                    getAppointmentID = Appointments.objects.get(id=id)
                    message = {
                        'id': getAppointmentID.id,
                        'PatientFirstName': getAppointmentID.Patient.PatientFirstName,
                        'PatientMiddleName': getAppointmentID.Patient.PatientMiddleName,
                        'PatientLastName': getAppointmentID.Patient.PatientLastName,
                        'PatientAge': getAppointmentID.Patient.PatientAge,
                        'PatientVillage': getAppointmentID.Patient.PatientVillage,
                        'PatientDistrict': getAppointmentID.Patient.PatientDistrict,
                        'PatientGender': getAppointmentID.Patient.PatientGender,
                        'PatientMobileNo': getAppointmentID.Patient.PatientMobileNo,
                        'Speciality': getAppointmentID.jobtypes.name,
                        'Speciality_id': getAppointmentID.jobtypes.id,
                        'AppointmentDate': getAppointmentID.AppointmentDate,
                        'Doctors': getAppointmentID.Doctor.get_full_name(),
                        'doctorid': getAppointmentID.Doctor.id,

                        
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                else:
                    return render('Hr/404.html')
            else:
                return render(request, 'Hr/404.html')

        if action == 'update_appointment':
            if request.user.has_perm('APEN.change_appointments'):
                # Get all data from the request
                AppointmentId = request.POST.get('AppointmentId')
                PatientFirstName = request.POST.get('PatientFirstName')
                PatientMiddleName = request.POST.get('PatientMiddleName')
                PatientLastName = request.POST.get('PatientLastName')
                PatientAge = request.POST.get('PatientAge')
                PatientVillage = request.POST.get('PatientVillage')
                Speciality = request.POST.get('jobtype_ids')
                AppointmentDate = request.POST.get('AppointmentDate')
                PatientGender = request.POST.get('PatientGender')
                PatientMobileNo = request.POST.get('PatientMobileNo')
                PatientDistrict = request.POST.get('PatientDistrict')
                Doctor = request.POST.get('Doctor')
                
                # Validaet data
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
                            'Message': 'Please enter text only',
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
                            'Message': 'Please enter text only',
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
                            'Message': 'Please enter text only',
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
                            'Message': 'Please enter text and nums only',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientVillage == '' or PatientVillage == 'null' or PatientVillage is None or PatientVillage == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Patient Village',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if text_validationNumber(PatientVillage) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter text and nums only',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if Speciality == '' or Speciality == 'null' or Speciality is None or Speciality == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select a Specialityt',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if AppointmentDate == '' or AppointmentDate == 'null' or AppointmentDate is None or AppointmentDate == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select an Appointment Date',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientMobileNo == '' or PatientMobileNo == 'null' or PatientMobileNo is None or PatientMobileNo == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Enter Patient\'s Mobile Number',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if number_validation(PatientMobileNo) == False:
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Please enter numbers only',
                            'title': 'Validation Error!',
                            'type': 'warning',
                        }
                    )
                if PatientDistrict == '' or PatientDistrict == 'null' or PatientDistrict is None or PatientDistrict == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select Patient\'s District',
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
                if Doctor == '' or Doctor == 'null' or Doctor is None or Doctor == 'undefined':
                    return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'Select a doctor',
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

                Update_Appointment = Appointments.objects.get(id=AppointmentId)
                get_patient = Patients.objects.get(id=Update_Appointment.Patient.id)
                get_doctor = Employee.objects.get(id=Doctor)
                get_Speciality = JobType.objects.get(id=Speciality)

                get_patient.PatientFirstName = PatientFirstName
                get_patient.PatientMiddleName = PatientMiddleName
                get_patient.PatientLastName = PatientLastName
                get_patient.PatientAge = PatientAge
                get_patient.PatientDistrict = PatientDistrict
                get_patient.PatientGender = PatientGender
                get_patient.PatientMobileNo = PatientMobileNo
                get_patient.PatientVillage = PatientVillage
                get_patient.save()

                Update_Appointment.Doctor = get_doctor
                Update_Appointment.jobtypes = get_Speciality
                Update_Appointment.AppointmentDate = AppointmentDate
                Update_Appointment.save()
                return JsonResponse(
                    {
                        'isError': False,
                        'Message': 'Appointment has been updated',
                        'title': 'Masha allah !' + Update_Appointment.Patient.PatientFirstName + "Info been updated",
                        'type': 'success',
                    }
                )
            else:
                return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to edit An Appointment ',
                            'title': 'No Access Permission',
                            'type': 'warning',

                        },
                    )
            
        if action == "get_jobtype_name":
            if request.user.has_perm('APEN.add_appointments'):
                jobtypeid = request.POST.get('jobtypeid')
                
                jobtype_data = JobType.objects.filter(id = jobtypeid)
                message = []
                for xspecilization in range(0, len(jobtype_data)):
                    message.append({
                        'id': jobtype_data[xspecilization].id,
                        'fullname': jobtype_data[xspecilization].name, 
                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            else:
                return render(request, 'Hr/404.html')
        if action == "get_Doctors_name":

            if request.user.has_perm('APEN.add_appointments'):
                jobtypeid = request.POST.get('jobtype_ids')    
                leavedoctors = '' 
                if Employee_Leave.objects.filter(State="Confirmed").values('employee').distinct().exists():
                    leavedoctors = Employee_Leave.objects.filter(State="Confirmed").values('employee').distinct()
                notshiftedtoday = Attandence.objects.filter(state = '0' ,today_date =currentDate).values('employee').distinct()             

                chosenEmployee = []
                jobtype_data = JobDetails.objects.filter(
                        ~Q(employee_type__icontains= "General-Director"),
                        ~Q(employee_type__icontains= "Director-Secretory"),              
                        ~Q(employee_type__icontains= "Department-Head"),                          
                        ~Q(employee__in = leavedoctors),
                        ~Q(employee__in = notshiftedtoday),                                        
                          job_type_id = jobtypeid,
                             is_active = True,
                            job_state = 'Approved' , 
                            employee__Employee_state = 'Approved',        
                            employee__is_terminated = False,                               
                            )

                message = []
                for selempl in jobtype_data:
                    empid = selempl.employee.id
                    existday = Manage_shift.objects.filter(employee_id = empid)               
                    for xperson in existday:   
                        days_in = xperson.shift.shift_date                    
                        days_in = days_in.split(',')            
                        day_name = currentDate.strftime("%A")                                               
                        for d in days_in:                            
                            if d == day_name:   
                                chosenEmployee.append(xperson.employee.id)    
                                break
                            else:
                                pass
              

                for xspecilization in range(0, len(jobtype_data)):
                    if jobtype_data[xspecilization].employee.id  in chosenEmployee:              
                        message.append({
                            'id': jobtype_data[xspecilization].id,
                            'employe_id': jobtype_data[xspecilization].employee.id,
                            'name': jobtype_data[xspecilization].employee.get_full_name(), 
                            'status': jobtype_data[xspecilization].employee.detect_attendance()
                        })
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            else:
               return render(request, 'Hr/404.html')

        if action == "get_appointment_info":
            if request.user.has_perm('APEN.view_appointments'):
                id = request.POST.get('appointId')                
                Appointment = Appointments.objects.get(id = id)               
                message = {
                    'AppointmentID': Appointment.AppointmentNumber,
                   
                    'PatientName':Appointment.Patient.get_fullName(),
                    'PatientAge': Appointment.Patient.PatientAge,
                    'PatientGender': Appointment.Patient.PatientGender,
                    'PatientMobileNo': Appointment.Patient.PatientMobileNo,
                    'PatientDistrict': Appointment.Patient.PatientDistrict,
                    'PatientVillage': Appointment.Patient.PatientVillage,
                    
                    'Doctor':Appointment.Doctor.get_full_name(),
                    'Status': Appointment.Status,
                    'AppointmentDate': Appointment.AppointmentDate,
                    'Receptionist_first': Appointment.Receptionist.first_name,
                    'Receptionist_last': Appointment.Receptionist.last_name,
                    'Queue_no': Appointment.queue_number,
                  
                }
                return JsonResponse({'isError': False, 'Message': message}, status=200)
            else:
                return render(request, 'Hr/404.html')
        if action == "getChartData":
            if request.user.has_perm('APEN.add_appointments'):
                year = request.POST.get('yearr')
                print(year, '.')
                completed_jan = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=1).count()
                cancelled_jan = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=1).count()
                all_jan = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=1).count()
                
                completed_feb = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=2).count()
                cancelled_feb = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=2).count()
                all_feb = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=2).count()

                completed_mar = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=3).count()
                cancelled_mar = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=3).count()
                all_mar = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=3).count()

                completed_april = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=4).count()
                cancelled_april = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=4).count()
                all_april = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=4).count()

                completed_may = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=5).count()
                cancelled_may = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=5).count()
                all_may = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=5).count()

                completed_jun = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=6).count()
                cancelled_jun = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=6).count()
                all_jun = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=6).count()

                completed_july = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=7).count()
                cancelled_july = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=7).count()
                all_july = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=7).count()
                
                completed_aug = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=8).count()
                cancelled_aug = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=8).count()
                all_aug = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=8).count()

                completed_sep = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=9).count()
                cancelled_sep = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=9).count()
                all_sep = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=9).count()

                completed_oct = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=10).count()
                cancelled_oct = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=10).count()
                all_oct = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=10).count()

                completed_nov = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=11).count()
                cancelled_nov = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=11).count()
                all_nov = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=11).count()

                completed_dec = Appointments.objects.filter(Status__icontains="Approved", AppointmentDate__year=year, AppointmentDate__month=12).count()
                cancelled_dec = Appointments.objects.filter(Status__icontains="Cancelled", AppointmentDate__year=year, AppointmentDate__month=12).count()
                all_dec = Appointments.objects.filter(AppointmentDate__year=year, AppointmentDate__month=12).count()

                message = {
                    'completed_jan': completed_jan,
                    'cancelled_jan': cancelled_jan,
                    'all_jan': all_jan,
                
                    'completed_feb': completed_feb,
                    'cancelled_feb': cancelled_feb,
                    'all_feb': all_feb,
                
                    'completed_mar': completed_mar,
                    'cancelled_mar': cancelled_mar,
                    'all_mar': all_mar,
                
                    'completed_april': completed_april,
                    'cancelled_april': cancelled_april,
                    'all_april': all_april,
                
                    'completed_may': completed_may,
                    'cancelled_may': cancelled_may,
                    'all_may': all_may,
                
                    'completed_jun': completed_jun,
                    'cancelled_jun': cancelled_jun,
                    'all_jun': all_jun,
                
                    'completed_july': completed_july,
                    'cancelled_july': cancelled_july,
                    'all_july': all_july,
                
                    'completed_aug': completed_aug,
                    'cancelled_aug': cancelled_aug,
                    'all_aug': all_aug,
                
                
                    'completed_sep': completed_sep,
                    'cancelled_sep': cancelled_sep,
                    'all_sep': all_sep,
                
                    'completed_oct': completed_oct,
                    'cancelled_oct': cancelled_oct,
                    'all_oct': all_oct,
                
                    'completed_nov': completed_nov,
                    'cancelled_nov': cancelled_nov,
                    'all_nov': all_nov,
                
                    'completed_dec': completed_dec,
                    'cancelled_dec': cancelled_dec,
                    'all_dec': all_dec,
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
def update_appointment_form(request, id):
    try:
        if request.user.has_perm('APEN.change_appointments'):
            is_exist = Appointments.objects.filter(id=id).exists()
            if is_exist:
                jobtypes = JobType.objects.all()
                Doctor = Employee.objects.all()
                Appointment = Appointments.objects.get(pk=id)
                districts = ['Dharkenley', 'Deynile', 'HowlWadaag', 'Wardhigley', 'Waaberi', 'HamarJajab', 'Bondhere', 'Karaan',
                            'Yaaqshid', 'Huriwaa', 'Kaxda', 'Hodan', 'Shibis', 'Abdiaziz', 'Shangani', 'Wadajir', 'HamarWeyne']
                Gender = ['Male', 'Female']

                context = {
                    'jobtypes': jobtypes,
                    'Doctors': Doctor,
                    'Appointment': Appointment,
                    'districts': districts,
                    'Genders': Gender,
                }
                return render(request, 'Appointments/Update-Appointment.html', context)
            else:
                return render(request, 'Hr/404.html')
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
def search_existing_patient(request, value):
    try:
        if request.user.has_perm('APEN.add_appointments'):
           
            existingPatient = Patients.objects.filter(
                Q(PatientFullName__istartswith = value)|
                Q(PatientMobileNo = value) 
                )
        
            message = []

            for xSearch in range(0, len(existingPatient)):

                message = {
                        'id': existingPatient[xSearch].id,                    
                        'PatientFirstName': existingPatient[xSearch].PatientFirstName,
                        'PatientMiddleName': existingPatient[xSearch].PatientMiddleName,
                        'PatientLastName': existingPatient[xSearch].PatientLastName,
                        'PatientAge': existingPatient[xSearch].PatientAge,
                        'PatientVillage': existingPatient[xSearch].PatientVillage,
                        'PatientMobileNo': existingPatient[xSearch].PatientMobileNo,
                        'PatientDistrict': existingPatient[xSearch].PatientDistrict,
                        'PatientGender': existingPatient[xSearch].PatientGender,
                    },
                
            return JsonResponse({'isError': False, 'Message': message}, status=200)
       
               
            return JsonResponse({'isError': False, 'Message': message}, status=200)
            # else:
            #     return render(request, 'Hr/404.html')
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
def approve_appointment(request, action):
    try:
        if action == "approve_appointment":
            if request.user.has_perm('APEN.Approve_appointment'):

                # Get all data from the request

                appointment_id = request.POST.get('appointmentId')
                status = request.POST.get('status')
                update_appointment = Appointments.objects.get(id=appointment_id)
                update_appointment.Status = status
            
                update_appointment.save()

                return JsonResponse(
                    {
                        'isError': False,
                        'Message': ' Approved Succesfully',
                        'title':  "The Appointment has been",
                        'type': 'success',
                    }
                    )
            else:
                return JsonResponse(
                        {
                            'isError': True,
                            'Message': 'You dont have permission to approve an Appointment ',
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
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)

@login_required(login_url='Login')
def SearchEngine(request):
    try:
        if request.user.has_perm('APEN.add_appointments'):
            search = request.POST.get('employee')
            searchFields = {}
            if request.method == 'POST':
                searchQuery = JobType.objects.filter(    
                        Q(name__icontains=search),
                        is_appoitment_rel = 'relate_appointment'
                        
                    )
                message = []
                for xSearch in range(0, len(searchQuery)):
                
                        message.append({
                            'label': f" {searchQuery[xSearch].name}",
                            'userid': searchQuery[xSearch].id,
                        },
                        )
                return JsonResponse({'Message': message}, status=200)
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

def GenerateAppointmentNumber():
    try:
        last_id = Appointments.objects.filter(~Q(AppointmentNumber=None)).last()
        serial = 0
        today = datetime.today().strftime('%d/%m/%y')
        today_without_slashes = today.replace('/', '')
        if last_id is not None:
            serial = int(last_id.AppointmentNumber[8:])
        serial = serial + 1

        if serial < 10:
            serial = '000' + str(serial)
        elif serial < 100:
            serial = '00' + str(serial)
        elif serial < 1000:
            serial = '0' + str(serial)

        return f"AP{today_without_slashes}{serial}"
    except Exception as error:
        message = {
            'title': 'Server Error!',
            'type': 'error',
            'isError': True,
            'Message': f'On Error Occurs {error}. Please try again or contact system administrator'
        }
        return JsonResponse(message, status=200)