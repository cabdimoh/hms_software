from django.urls import path
from . import views
from  . import Employee
from . import hrRequirements
from . import exitemployee
from . import employee_requirements
from . import management
from . import payroll



urlpatterns = [
    
    path('employee_lists', Employee.employees, name='employees'),
    path('employee_galery', Employee.employeGalery, name='employees_galery'),
    path('Pending_employee_lists', Employee.Pending_employees, name='Pending_employee_list'),
    path('employee_detail/<str:pk>', Employee.view_Employee, name='employee_details'),


    path('manage_employees/<str:action>', Employee.manage_employee),
    path('printEmployee', Employee.printEmployeeData,name="printemployee_data"),
    path('manage_Experience/<str:action>', employee_requirements.manage_Experience),
    path('manage_qualification/<str:action>', employee_requirements.manage_Qualification),
    path('manage_Job_Detail/<str:action>', employee_requirements.manage_JobDetail),
    path('manage_EmployeeAccountk/<str:action>', employee_requirements.manage_EmployeeAccount),




    path('prerequirements/', hrRequirements.view_all_prerequirements, name="prequirements"),
    path('prerequirements/<str:action>', hrRequirements.manage_requirements),
    path('hrm-report/', hrRequirements.hrmReportview, name="hrm_report"),


    # employee leave    
    path('view_Leave_Cotegory/', exitemployee.viewLeaveCotegroy, name="view_leave_cotegory"),
    path('Leave_cotegory_all/<str:activity>', exitemployee.manage_Leave_cotegory),

    path('leaves_employees/', exitemployee.view_Leave_Employe, name="view_leave_employee"),
    path('leave_employee_all/<str:activity>', exitemployee.manage_Leave_employee),
 

    path('view_Cotegory/', exitemployee.viewExitCotegroy, name="view_exit_cotegory"),
    path('exit_cotegory_all/<str:activity>', exitemployee.manage_exit_cotegory),

    path('veiw_exit_employee/', exitemployee.view_Exit_Employe, name="view_exit_employee"),
    path('exit_employee_all/<str:activity>', exitemployee.manage_exit_employee),
 
    path('veiw_Death_employee/', exitemployee.view_Death_Employe, name="view_Death_employee"),



    # pendingJobs
    path('veiw_pendingJobs/', employee_requirements.view_PendingJobs_Employe , name="view_PendingJobs"),
    path('manage_pending_jobs/<str:activity>', employee_requirements.manage_PendingJobs_employee),
    path('printEmployeeJob/<int:id>/', employee_requirements.printDetail , name="printjobs"),




    path('search_engine/', exitemployee.SearchEngine , name="search_user" ),
    path('dapartments/', management.departments , name="all_departments" ),
    path('createshifts/', management.CreateShift , name="createshift" ),
    path('management_setup/', management.Management_setup , name="Manageemnt_setup" ),
    # path('manage_setup/<str:activity>', management.Manage_setup , name="Manage_setup" ),attendanceAction

    path('view_shift/<str:id>', management.view_shift , name="view_shifts" ),
    path('manages_shifts/<str:activity>', management.management_shift , name="manage_shifts" ),
    path('search_employee/', management.SearchEmployee , name="search_employees" ),
    path('attendance/', management.attendance , name="attendance_list" ),
    path('attendancelist/', management.attendanceAction , name="attendance_report" ),
    path('manageshiftlist/<str:activity>', management.manage_Attendance , name="attendance_manege" ),



    # payroll payroll

    path('Payroll-list/', payroll.view_payroll, name="viewPayroll"),





]
