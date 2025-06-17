from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.static import serve
from django.urls import re_path


urlpatterns = [

    path('', lambda request: redirect('adminlogin')),

    # Permission URLs
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
    path('permissions/create/', PermissionCreateView.as_view(), name='permission_create'),
    path('permissions/<int:pk>/edit/', PermissionEditView.as_view(), name='permission_edit'),
    path('permissions/<int:pk>/delete/', PermissionDeleteView.as_view(), name='permission_delete'),

    #Login URL
    path('adminlogin/', LoginFormView,name="adminlogin"),
    #Dashboard URL
    path('Dashboard/', Dashboard.as_view(),name="view_dashboard"),
    #Logout URL
    path('logout/', logout_view, name='logout'),  # Add the logout path here

    # forgot password URL
    path('forgot-password/', ForgotPasswordAdminView.as_view(), name='Forgot_Password_Admin'),
    path('verify-otp-admin/', VerifyOTPAdminView.as_view(), name='verify_otp_admin'),
    path('reset-password-admin/', ResetPasswordAdminView.as_view(), name='reset_password_admin'),

    path('System-Settings/', System_Settings.as_view(),name="System_Settings"),
    path('user_profile/',UserProfileView.as_view(),name='user_profile'),
    path('edit_profile/', UserUpdateProfileView.as_view(), name='edit_profile'),
    path('change_password_ajax/', change_password_ajax, name='change_password_ajax'),


    #User Role URL
    path('user-roles/', RoleView.as_view(), name='role_list'),
    path('user-role/create/', RoleCreateView.as_view(), name='role_create'),
    path('user-role/edit/<int:role_id>/', RoleEditView.as_view(), name='role_edit'),
    path('user-role/delete/<int:role_id>/', RoleDeleteView.as_view(), name='role_delete'),

    # Role Permission URLs
    path('user-roles/based-permissions/<int:role_id>/', RolePermissionView.as_view(), name='role_permissions'),
    
    # User Management URLs
    path('default-user/', DefaultUserList.as_view(), name='default_user_list'),
    path('default-user/detail/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('default-user/user/<int:pk>/toggle-status/', ToggleUserStatusView.as_view(), name='user_toggle_status'),
    
    # Module URLs
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('modules/create/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/edit/<int:pk>/', ModuleEditView.as_view(), name='module_edit'),
    path('modules/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),

    # SubAdmin URLs
    path('subadmins/', SubAdminListView.as_view(), name='subadmin_list'),
    path('subadmins/detail/<int:user_id>/', UserDetailView.as_view(), name='subadmin_detail'),

    # SubAdmin Create, Edit, Toggle Status, and Delete URLs
    path('subadmins/create/', SubAdminCreateView.as_view(), name='subadmin_create'),
    path('subadmins/<int:pk>/edit/', SubAdminEditView.as_view(), name='subadmin_edit'),
    path('subadmins/<int:pk>/toggle-status/', SubAdminToggleStatusView.as_view(), name='subadmin_toggle_status'),
    path('subadmins/<int:pk>/delete/', SubAdminDeleteView.as_view(), name='subadmin_delete'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
