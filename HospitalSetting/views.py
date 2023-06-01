from django.shortcuts import render
from APEN.models import *
from Hr.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required(login_url='Login')
def dashboard(request):
    spclty_with_appoint_count={}
    specialities = JobType.objects.filter(Q(is_appoitment_rel__icontains="relate_appointment"))
    for speciality in specialities:
        get_specialitys_appointment = Appointments.objects.filter(jobtypes=speciality.id).count()
        special_count = {
            speciality.name : get_specialitys_appointment
        }

        spclty_with_appoint_count.update(special_count)
    EmployeeList = Employee.objects.filter(
            Employee_state="Approved", is_terminated=False)
    AppointmentList = Appointments.objects.all().order_by('-AppointmentDate')[:3]
    
    patients = Patients.objects.all()
    patients_count = Patients.objects.all().count()
    appointments = Appointments.objects.all().count()
    emrgency = EmergencyRoomVisit.objects.all().count()
    new_patient = (appointments +emrgency)- patients_count
    new_patient =[]
    old_patient = []
    for patient in patients:
        get_patients_appoint = Appointments.objects.filter(Patient=patient.id).count()
        if get_patients_appoint == 1:
            new_patient.append(get_patients_appoint)
        elif get_patients_appoint >1:
            old_patient.append(get_patients_appoint)
    
    new_patients = len(new_patient)+emrgency
    old_patients = len(old_patient)

    getdoctors = JobDetails.objects.filter(job_type__is_appoitment_rel = 'relate_appointment').values('employee').distinct()
    getallstaff = JobDetails.objects.filter(is_active = True, job_state = 'Approved').values('employee').distinct()
   
    context = {
        'emrgency':emrgency,
        'appointments':appointments,
        'specialities':specialities,
        'spclty_with_appoint_count':spclty_with_appoint_count,
        'EmployeeList':EmployeeList,
        'AppointmentList':AppointmentList,
        'old_patients':old_patients,
        'new_patients':new_patients,
        'patients_count':patients_count,
        'EmployeeCount': Employee.objects.filter(Q(id__in= getallstaff),is_terminated = False, Employee_state = "Approved").count(),
        'DoctorCount': Employee.objects.filter(Q(id__in = getdoctors), is_terminated = False, Employee_state = "Approved").count(),
       
    }
    return render(request, 'dashboard.html', context)
