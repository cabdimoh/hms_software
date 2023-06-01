from django.urls import path
from . import views 
from . import equipment
from . import medicine


urlpatterns = [

    # path('dashbord', views.dashbord, name='dashbord'),
    #-----------medicine-----------
    path('medicines', medicine.MedicineList, name='medicines'),
    path('delete-medicine/<Medicine_id>', medicine.delete_medicine, name='delete_medicine'),
    path('delete-category/<Medicine_categories_id>', medicine.delete_category, name='delete_category'),
    path('Expaire-medicine-list', medicine.Expaire_medicine_list, name='Expaire-medicine-list'),

    # path('medicicne-in', medicine.medicine_in, name='medicicne-in'),
    
    path('manage-medicine/<str:action>', medicine.manage_medicine, name='manage_medicine'),
    path('manage-category/<str:action>', medicine.manage_category, name='manage_category'),
    path('medicine-category', medicine.Medicine_category, name='Medicine_category'),
    
    #------meicine orders--------
    path('medicine-order', views.medicine_order, name='medicine-order'),
    path('manage-order-medicine/<str:action>', views.manage_order_medicine, name='manage-order-medicine'),
    path('medicine-View/<str:pk>', medicine.view_medicine, name='medicine-View1'),
    #------equipment order---------
    path('equipment-order', equipment.equipment_order, name='equipment-order'),
    path('manage-order-equipment/<str:action>', equipment.manage_order_equipment, name='manage-order-equipment'),
    
    #---------equipment--------
    path('equipment-categories', equipment.equipment_categories, name='equipment_categories'),
    path('manage-equipment-cat/<str:action>', equipment.manage_equipment_cat, name='manage_equipment_cat'),
    path('delete-equipment-category/<delete_equipment_category_id>', equipment.delete_equipment_category, name='delete_equipment_category'),
    path('manage-equipment/<str:action>', equipment.manage_equipment, name='manage_equipment'),
    path('equipment', equipment.equipment, name='equipment'),
    path('delete-equipment/<Equipment_id>', equipment.delete_equipment, name='delete_equipment'),
    path('equipment-View/<str:pk>', equipment.view_equipment, name='equipment-View'),
    path('lost-and-dameged', equipment.Lost_and_damed, name='lost-and-dameged'),
    path('manage-lost-damage-equipment/<str:action>', equipment.manage_lost_and_damage_equipment, name='manage-lost-damage-equipment'),
]

