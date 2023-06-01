from django.urls import path
from . import views
from . import appointment
from . import inpatient
from . import outpatient
from . import emergency
from . import Room_and_Beds


urlpatterns = [
    path('appointment-list', appointment.appointment_list, name = "Appointment-list"),
    path('cancelled-appointment-list', appointment.cancelled_appointment_list, name = "cancelled-Appointment"),
    path('add-appointment', appointment.add_appointments, name = "Add_Appointment"),
    path('manage-appointment/<str:action>', appointment.manage_appointment),
    path('update-appointment-form/<id>', appointment.update_appointment_form, name = "Update-Appointment-Form"),
    path('search-existing-patient/<str:value>', appointment.search_existing_patient, name = "SearchExistingPatient"),
    path('approve-appointment/<str:action>', appointment.approve_appointment),
    path('search_speciality/', appointment.SearchEngine, ),


    path('outpatient-list', outpatient.outpatient_list, name = "Outpatient-list"),
    path('patient-View/<id>', outpatient.patient_view, name = "patient-view"),
    path('manage-prescription/<str:action>', outpatient.manage_prescription),
    path('manage-patient-operation/<str:action>', outpatient.manage_patient_operation),
    path('manage-patient-diagnosis/<str:action>', outpatient.manage_patient_diagnosis),
    path('order-admission/<str:action>', outpatient.order_admission),


   
    
    # views file
    path('operations-category', views.category_operations_list, name="operations_category"),
    path('manage-category/<str:action>', views.manage_category_operations, name="manage_category"),
    
    path('operations', views.operations_list, name="operations"),
    path('manage-operations/<str:action>', views.manage_operations, name="manage_operations"),


    #--------------------Room and Beds -----------------------------------------------------#
     path('room-category', Room_and_Beds.room_category, name="room-category"),
     path('manage-room-category/<str:action>', Room_and_Beds.manage_room_category, name="manage-room-category"),
     path('add-room', Room_and_Beds.add_room, name="add-room"),
     path('manage-room/<str:action>', Room_and_Beds.manage_room, name="manage-room"),
     path('room-view/<str:pk>', Room_and_Beds.room_view, name='room-view'),
     path('add-bed', Room_and_Beds.add_bed, name="add-bed"),
     path('manage-bed/<str:action>', Room_and_Beds.manage_bed, name="manage-bed"),

    # emergency 
    path('emergency-queue', emergency.emergency_queue_list, name="emergency-queue"),
    path('in-treatment-patients', emergency.intreatment_list, name="in-treatment-patients"),
    path('triage-form/<str:pk>', emergency.triage_form, name="triage-form"),
    path('manage-emergency-profile/<str:action>', emergency.manage_emergency_profile, name="manage-emergency-profile"),
    path('manage-emergency-prescription/<str:action>', emergency.manage_prescription),
    path('manage-emergency-patient-diagnosis/<str:action>', emergency.manage_patient_diagnosis),
    path('dishcarged-patients-list', emergency.emergency_discharged_patients_list, name="emergency-discharged-patients"),
    path('approve-visit/<str:action>', emergency.approve_visit),

    # ------------------------------inpatient --------------
    path('admission-orders-list', inpatient.ordered_admissions, name = "admission-order"),
    path('manage-ordered-admission/<str:action>', inpatient.manage_ordered_admissions, name = "manage-admission-order"),
    path('inpatient-list', inpatient.inpatient_list, name = "Inpatient-list"),
    path('inpatient-vieew/<int:admission_id>/', inpatient.inpatient_view_appointment, name='Inpatient-view-appointment'),
    path('inpatient-view/<int:admission_id>/', inpatient.inpatient_view_emergency, name='Inpatient-view-emergency'),
    path('manage-inpatient-prescription/<str:action>', inpatient.manage_prescription),
    path('manage-inpatient-diagnosis/<str:action>', inpatient.manage_patient_diagnosis),
    path('manage-inpatient-operation/<str:action>', inpatient.manage_patient_operation),
    path('manage-inpatient-profile/<str:action>', inpatient.manage_patient_profile),
    path('discharged-inpatients', inpatient.discharged_inpatients_list, name="discharged-inpatients"),


]