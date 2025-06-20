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
    path('default-user/detail/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('default-user/user/<int:pk>/toggle-status/', ToggleUserStatusView.as_view(), name='user_toggle_status'),
    
    # Module URLs
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('modules/create/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/edit/<int:pk>/', ModuleEditView.as_view(), name='module_edit'),
    path('modules/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),

    # URLs
    path('customers/', ActiveCustomerListView.as_view(), name='customer_list'),
    path('Inactive/customer/', InactiveCustomerListView.as_view(), name='inactive_customers'),
    path('customers/detail/<int:user_id>/', UserDetailView.as_view(), name='customer_detail'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', CustomerEditView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/toggle-status/', CustomerToggleStatusView.as_view(), name='customer_toggle_status'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),

    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:pk>/edit/', InvoiceEditView.as_view(), name='invoice_edit'),
    path('invoices/<int:pk>/pdf/', InvoicePdfView.as_view(), name='invoice_pdf'),
    path('invoices/<int:pk>/print/', print_invoice, name='invoice_print'),
    path('invoices/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
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
