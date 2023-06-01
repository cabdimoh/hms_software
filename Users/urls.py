from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('add-users', views.EmployeeList, name='Users'),
    path('users-management/<str:action>', views.Manage_user, ),

    path('user-lists', views.UsersList, name='UsersList'),
    # Audit and logs
    path('audit_trials', views.AuditTrialss, name='AuditTrials'),
    path('Login_user', views.Login, name='Login'),
    path('Logout_user', views.Logout, name='Logout'),
    path('Logout_users', views.LoggedOut, name='Logout_user'),
    path('user-profile', views.userProfile, name='user_profile_all'),
    path('error-logs', views.ErrorLogss, name='ErrorLogs'),
    path('manage-error-log/<str:action>', views.ManageErrorLogs),


    # Roles
    path('user_roles_report', views.ViewUserRolesReportPage, name='UserRolesReport'),
    path('search_role', views.SearchRole, name='SearchRole'),
    path('search_engine_all/<str:search>/<str:type>', views.SearchEngineUser, name='search_user'),
    path('roles_report', views.ViewRolesReportPage, name='RolesReport'),
    path('single_roles', views.ViewRolesPage, name='SingleRoles'),
    path('group_roles', views.ViewGroupRolesPage, name='GroupRoles'),
    path('manage_group', views.ViewManageGroupPage, name='ManageGroup'),
    path('edit_group/<int:group_id>', views.ViewEditGroupPage, name='EditGroup'),
    path('manage_permission/<str:id>',views.ManagePermission, name='ManageRoles'),
    path('manage_permission_report',views.PermissonReport, name='PermissonReport'),
    path('manage_group_permission/<str:id>/<str:_id>', views.ManageGroupPermission, name='ManageGroups'),
    path('manage_group/<str:id>',views.ManageGroup),
    path('rename_group', views.RenameGroup),
    # path('print_user_roles/<str:id>', views.PrintUserRole, name='PrintUserRole'),

]
