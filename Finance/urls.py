from django.urls import path
from . import views
from . import Income

urlpatterns = [
    # main Account
    path('mainAccounts/', Income.main_account, name='main_account'),
    path('manage-mainAccounts/<str:activity>', Income.ManageMainAccount, name='main_account'),


    # income source 
    path('Income-source/', Income.incomeSources, name='incomeSource'),
    path('manage-income-source/<str:activity>', Income.ManageIncomeSource, name='incomesources'),
    

#  Manage_transfer_cash
    # cash transfer    
    path('income-transfer/', Income.cashtransfer, name='cashtransfer'),
    path('manage-transfer-income-source/<str:activity>', Income.Manage_transfer_cash, name='incomesources'),



]