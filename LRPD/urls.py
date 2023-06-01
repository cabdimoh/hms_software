from django.urls import path
from . import views
from . import LabResult
from . import labRegistraion
from . import doctor
from . import radiology
from . import pharmacy

urlpatterns = [
    #------------------lab Registration---------------------------
    path('manage-lab-setup/<str:action>', labRegistraion.manage_lab_setup, name='manage-lab-setup'),
    path('view-lab-setup', labRegistraion.view_lab_setup, name='view-lab-setup'),
    path('lab-tests', labRegistraion.LabTests_list, name='LabTests-list'),
    path('manage-lab-test/<str:action>', labRegistraion.manage_labtest),
    
    #------------------lab Resutl---------------------------
    path('lab-test-orders', LabResult.lab_test_orders, name='Lab-Test-Orders'),
    path('lab-result', LabResult.lab_result, name='Lab-Result'),
    path('add-lab-result-form/<str:pk>', LabResult.add_lab_result_form, name='add-lab-result-form'),
    path('manage-labresult/<str:action>', LabResult.manage_labresult),
    path('update-lab-result-form/<str:pk>', LabResult.edit_lab_result_form, name='update-lab-result-form'),

   
    #------------------doctor---------------------------
    path("doctor-appontment/", doctor.doctor_appointments, name="doctor_appontments"),
    path('doctor-list/', doctor.doctor_list, name="doctor_list"),

    #------------------lab making order to store in views.py---------------------------
    path('lab-equipment-order', views.lab_equipment_order, name='lab-equipment-order'),
    path('manage-lab-equipment-order/<str:action>', views.manage_lab_equipment_order, name='manage-lab-equipment-order'),
    
  
    #---------------------pharmacy------------------------#
    path('order-medicine', pharmacy.order_medicine, name='order-medicine'),
    path('doctor-order', pharmacy.doctor_order, name='doctor-order'),
    path('manage-doctor-order/<str:action>', pharmacy.Manage_doctor_order),
    path('manage-medicine-order/<str:action>', pharmacy.manage_medicine_order),
    path('medicine-list', pharmacy.medicine_list, name='medicine-list'),
    path('view-medicine/<str:pk>', pharmacy.view_medicine, name='view-medicine'),
    path('Expaire-medicine-pharmacy', pharmacy.Expaire_medicine_pharmacy, name='Expaire-medicine-pharmacy'),
    path('print-pharmacy', pharmacy.print_pharmacy, name='print-pharmacy'),

    
    #------------------Radiology---------------------------
    path('radiology-exam-orders', radiology.radiology_exam_orders, name='radiology-Exam-Orders'),
    path('radiology-result', radiology.radiology_result, name='Radiology-Result'),
    path('radiology-exam', radiology.RadiologyExam_list, name='RadiologyExam-list'),
    path('manage-radiology-exam/<str:action>', radiology.manage_RadiologyExam),
    path('manage-radiology-result/<str:action>', radiology.manage_radiologyresult),
    path('manage-dropdown/<str:action>', radiology.manage_dropdown),
    path('manage-category/<str:action>', radiology.manage_category_radiology, name="manage_category"),
    path('exam-category', radiology.exam_category_list, name="exam_category"),
    path('add-radio-result-form/<str:pk>', radiology.add_radio_result_form, name='add-radio-result-form'),
    path('radiology-equipment-order', radiology.radiology_equipment_order, name='radiology-equipment-order'),
    path('manage-radiology-equipment-order/<str:action>', radiology.manage_radiology_equipment_order, name='manage-radiology-equipment-order'),
    path('update-radio-result-form/<str:pk>', radiology.edit_radio_result_form, name='update-radio-result-form'),

    #  path('out-of-pharmacy', pharmacy.out_of_pharmacy, name='out-of-pharmacy'),
    
   
    


    

    

]