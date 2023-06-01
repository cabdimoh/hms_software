from django.db import models
from Hr.models import Employee 
from django.urls import reverse
from Inventory.models import Medicine 
from Hr.models import JobType
# from LRPD.models import Medicine , pharmacy_medicine
from Users.models import Users
# Create your models here.
Gender_type = (
    ('Female', 'Female'),
    ('Male', 'Male'),

)
class Specialities(models.Model):    
    specialization_name = models.CharField(max_length=100)    
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.specialization_name

 

class Patients(models.Model):
    PatientFirstName = models.CharField(max_length=60)
    PatientMiddleName = models.CharField(max_length=60)
    PatientLastName = models.CharField(max_length=60)
    PatientFullName = models.CharField(max_length=100)
    PatientAge = models.CharField(max_length=60)
    PatientGender = models.CharField(max_length=60)
    PatientMobileNo = models.CharField(max_length=50, null=True, blank=True)    
    PatientVillage = models.CharField(max_length=100, null=True, blank=True)
    PatientDistrict = models.CharField(max_length=100, null=True, blank=True)
    PatientMaritalStatus = models.CharField(max_length=100)
    class Meta:
        db_table = 'Patients'

    def get_fullName(self):
        return f"{self.PatientFirstName} {self.PatientMiddleName} {self.PatientLastName}"
    
    def __str__(self):
        return self.PatientFirstName
   
class Appointments(models.Model):
    AppointmentDate = models.DateField()
    Patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='Doctor')
    jobtypes = models.ForeignKey(JobType, on_delete=models.RESTRICT, null=True)
    Receptionist = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, related_name='Receptionist')
    Status = models.CharField(max_length=50)
    AppointmentNumber = models.CharField(max_length=100)
    queue_number = models.IntegerField()
    class Meta: 
        db_table = 'Appointments'

    def __str__(self):
        return self.Patient.get_fullName

    def save(self, *args, **kwargs):
        if not self.pk or self.Doctor != self.__class__.objects.get(pk=self.pk).Doctor:
            # Get the number of appointments for this doctor today
            today_appointments_count = Appointments.objects.filter(Doctor=self.Doctor, AppointmentDate=self.AppointmentDate).count()

            # Set the queue number for the appointment
            self.queue_number = today_appointments_count + 1

        super(Appointments, self).save(*args, **kwargs)
    class Meta:
        permissions = [
            ("Approve_appointment", "Can approve Appointment"),
        ]

class OperationCategory(models.Model):
    CategoryName = models.CharField(max_length=100)
    Description = models.CharField(max_length=100) 
    class Meta:
        db_table = 'OperationCategory'
        
    def _str_(self):
        return self.CategoryName 
    
class Operations(models.Model):
    OperationName = models.CharField(max_length=150)
    CategoryName = models.ForeignKey(OperationCategory, on_delete=models.SET_NULL, null=True)
    Description = models.CharField(max_length=200)
    class Meta:
        db_table = 'Operations'
        
    def _str_(self):
        return self.OperationName


class EmergencyRoomVisit(models.Model):
    Patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    VisitDateTime = models.DateTimeField(auto_now_add=True)
    DischargeDateTime = models.DateTimeField(blank=True, null=True)
    EmergencyNumber = models.CharField(max_length=10, null=True, blank=True)    
    EmergencyName = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    VisitNumber = models.CharField(max_length=100)
    class Meta:
        db_table = 'EmergencyRoomVisit'
    
    def __str__(self):
        return self.id
    def get_absolute_url(self):
        return reverse('triage-form', args=[self.id])
    class Meta:
        permissions = [
            ("Approve_visit", "Can approve EmergencyVisit"),
        ]
class EmergencyTriage(models.Model):
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.CASCADE)
    ChiefComplaint = models.TextField()
    Allergies = models.TextField()
    Vitalsigns = models.TextField()
    CurrentMedications = models.TextField()
    FamilyMedicalHistory = models.TextField()
    PastMedicalHistory = models.TextField()
    Triage_dateTime = models.DateTimeField()
    Doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='emergency_Doctor')
    TriageCategory = models.CharField(max_length=60)
    Assessment = models.TextField()
    TriageNurse = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='Triage_nurse')
    Comment = models.TextField()

  
    class Meta:
        db_table = 'EmergencyTriage'

    def __str__(self):
        return self.id



#--------Romm-----AND-----------Beds---------------
    
class Room_category(models.Model):
    department = models.ForeignKey('Hr.Departments', on_delete=models.SET_NULL, null=True)
    Category_name = models.CharField(max_length=100)
    Discription = models.CharField(max_length=100)

    class Meta:
        db_table = 'Room_category'
        
    def _str_(self):
        return self.Category_name


class Room(models.Model):
    Room_category = models.ForeignKey(Room_category, on_delete=models.SET_NULL, null=True)
    Room_NO = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def get_room_details_url(self):
        return reverse('room-view', args=[self.id])

    class Meta:
        db_table = 'Room'
        
    def _str_(self):
        return self.Room_NO
    
class Beds(models.Model):
    Room = models.ForeignKey(Room,on_delete=models.SET_NULL, null=True)
    BedNO = models.CharField(max_length=300)
    status = models.CharField(max_length=20)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
        
    #     if self.Room and self.Room.BedNO_set.filter(status='Occupied').count() == self.Room.BedNO_set.count():
    #         self.Room.status = 'full'
    #         self.Room.save()

    class Meta:
        db_table = 'Beds'
        
    def _str_(self):
        return self.BedNO


class AdmissionOrder(models.Model):
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.SET_NULL, null=True)
    Appointment = models.ForeignKey(Appointments, on_delete=models.SET_NULL, null=True)
    Ordered_by = models.CharField(max_length=100)
    AdmissionDate = models.DateField()
    AdmissionReason = models.TextField()
    BedType = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    Note = models.TextField()
    patient_priority = models.CharField(max_length=100)

    class Meta:
        db_table = 'AdmissionOrder'
        
    def _str_(self):
        return self.id

class Addmission(models.Model):
    Admission_order = models.ForeignKey(AdmissionOrder, on_delete=models.SET_NULL, null=True)
    GuardianName = models.CharField(max_length=80)
    GuardianMobileNo = models.CharField(max_length=80)
    GuardianRelship = models.CharField(max_length=80)
    GuardianAddress = models.CharField(max_length=100)
    DischargeDate = models.DateTimeField(null=True, blank=True)
    Status = models.CharField(max_length=70)
    AddmissionNumber = models.CharField(max_length=100)
    AddmissionDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Addmission'
        
    def _str_(self):
        return self.id
    
class Referrel(models.Model): 
    HospitalName = models.TextField()
    Referel_Date = models.DateField()
    Referel_Reason = models.TextField()
    class Meta:
        db_table = 'Referrel'
        
    def _str_(self):
        return self.id
    
class PatientDeath(models.Model):
    Death_Date = models.DateTimeField()
    Death_Reason = models.TextField()
    class Meta:
        db_table = 'PatientDeath'
        
    def _str_(self):
        return self.id
class Discharge(models.Model): 
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.SET_NULL, null=True)
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    dischargeStatus = models.CharField(max_length=100)
    Operation = models.TextField()
    Note = models.TextField()
    Diagnosis = models.TextField()
    referrel = models.ForeignKey(Referrel, on_delete=models.SET_NULL, null=True)
    death = models.ForeignKey(PatientDeath, on_delete=models.SET_NULL, null=True)
    Admission_order = models.ForeignKey(AdmissionOrder, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'Discharge'
        
    def _str_(self):
        return self.id
    


# medicine prescription 

class MedicinesPrescription(models.Model):
    Appointment = models.ForeignKey(Appointments, on_delete=models.SET_NULL, null=True)
    Prescription_Date = models.DateField(auto_now_add=True)
    Status = models.CharField(max_length=100)
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.SET_NULL, null=True)
    Ordered_by = models.TextField()    
    PrescriptionNo = models.CharField(max_length=100)
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    instructions = models.TextField()    

    class Meta:
        db_table = 'MedicinesPrescription'
        
    def _str_(self):
        return self.Appointment.Patient.get_fullName
    
class MedicinePrescriptionDetials(models.Model):
    PrescriptionNo = models.ForeignKey(MedicinesPrescription, on_delete=models.CASCADE)
    MedicineName = models.ForeignKey('LRPD.pharmacy_medicine', on_delete=models.SET_NULL, null=True)
    Quantity = models.IntegerField()
    Dose = models.CharField(max_length=100)
    DoseInterval = models.CharField(max_length=150)
    DoseDuration = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'MedicinePrescriptionDetials'
        
    def _str_(self):
        return self.PrescriptionNo
    


class MedicationDose(models.Model):
    Medication_date = models.DateField()
    Medicition_time = models.TimeField()
    Medication_name = models.ForeignKey(MedicinePrescriptionDetials, on_delete=models.CASCADE)
    Medication_dose = models.CharField(max_length=100)
    Medicition_Remarks = models.TextField()
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.SET_NULL, null=True)


    class Meta:
        db_table = 'MedicationDose'
        
    def _str_(self):
        return self.id
    


class Patient_operation(models.Model):
    Appointment = models.ForeignKey(Appointments,  on_delete=models.SET_NULL, null=True)
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    Operation = models.ForeignKey(Operations, on_delete=models.RESTRICT)
    OperationDate = models.DateField()
    Status = models.CharField(max_length=100)
    class Meta: 
        db_table = 'Patient_operation'

    def __str__(self):
        return self.Appointment.Patient.get_fullName
       
class NurseNotes(models.Model):
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    Note_dateTime = models.DateTimeField()
    Nurse = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    Note = models.TextField()
    Comment = models.TextField()
    class Meta: 
        db_table = 'NurseNotes'

    def __str__(self):
        return self.Admission.id
    

    
class AssignBed(models.Model):
    Visit = models.ForeignKey(EmergencyRoomVisit, on_delete=models.SET_NULL, null=True)
    Room = models.ForeignKey(Room,on_delete=models.CASCADE)
    Bed = models.ForeignKey(Beds,on_delete=models.CASCADE)
    FromDate = models.DateTimeField()
    ToDate = models.DateTimeField(null=True, blank=True)
    Admission = models.ForeignKey(Addmission, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'AssignBed'
        
    def _str_(self):
        return self.id

