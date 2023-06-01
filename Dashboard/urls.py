from django.urls import path

from .import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    # path('', views.dashbord, name='dashboard'),
    # #  path('medicines', medicine.MedicineList, name='medicines'),
]