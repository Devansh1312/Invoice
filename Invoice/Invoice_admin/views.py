# Standard library imports
import csv
import os
import random
import json
from datetime import timedelta
from functools import wraps
from django.utils.crypto import get_random_string

# Django core imports
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils.translation import gettext as _, activate
from django.core.files.storage import FileSystemStorage, default_storage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Avg, Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View

# Django REST framework imports
from rest_framework.views import APIView

# Project specific imports
from Invoice_admin.models import *
from Invoice_admin.forms import *
from Invoice_admin.decorators import permission_required
from Invoice.firebase_config import send_push_notification

# Send email to sub-admin with details
def send_sub_admin_detail(email, name,username,password,subject):
    system_settings = SystemSettings.objects.first()
    logo = system_settings.footer_logo if system_settings and system_settings.footer_logo else ''
    context = {
        'name': name,
        'username': username,
        'password': password,
        'language': 'en',
        'logo': logo,
    }
    # Render HTML template
    html_content = render_to_string('Admin/Emails/Sub_Admin_Create.html', context)
    
    # Create plain text version (optional but recommended)
    text_content = strip_tags(html_content)
    
    # Create email
    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    email_msg.attach_alternative(html_content, "text/html")
    
    try:
        email_msg.send()
        return True
    except Exception as e:
        return False

# Role Permission View
@method_decorator(permission_required('role_permissions'), name='dispatch')
class RolePermissionView(View):
    def get(self, request, role_id):
        role = Role.objects.get(pk=role_id)
        modules = Modules.objects.prefetch_related('permission_set').all().order_by('name_en')
        role_permissions = role.permissions.all().order_by('display_name')
        
        # Create a dictionary to organize permissions by module
        module_permissions = []
        for module in modules:
            permissions = module.permission_set.all()
            if permissions.exists():
                module_permissions.append({
                    'module': module,
                    'permissions': permissions,
                    'has_permissions': True
                })
        
        # Get permissions without modules
        no_module_permissions = Permission.objects.filter(module__isnull=True)
        if no_module_permissions.exists():
            module_permissions.append({
                'module': None,
                'permissions': no_module_permissions,
                'has_permissions': True
            })
        
        return render(request, 'Admin/Permissions/permissions.html', {
            'role': role,
            'module_permissions': module_permissions,
            'role_permissions': role_permissions,
            'breadcrumb': {'parent': 'Admin', 'child': 'Role Permissions'}
        })

    def post(self, request, role_id):
        role = Role.objects.get(pk=role_id)
        selected_permissions = request.POST.getlist('permissions')
        
        # Clear existing permissions
        RoleHasPermission.objects.filter(role=role).delete()
        
        # Add new permissions
        for perm_id in selected_permissions:
            permission = Permission.objects.get(pk=perm_id)
            RoleHasPermission.objects.create(role=role, permission=permission)
        
        messages.success(request, 'Permissions updated successfully')
        return redirect('role_permissions', role_id=role.id)

##################################################################################
# Permission Views
##################################################################################

@method_decorator(permission_required('permission_list'), name='dispatch')
class PermissionListView(View):
    def get(self, request):
        permissions = Permission.objects.select_related('module').all()
        modules = Modules.objects.all()
        return render(request, 'Admin/Permissions/Permissions_List.html', {
            'permissions': permissions,
            'modules': modules,
            'breadcrumb': {'child': 'Permission Management'}
        })
    
# Permission Create View
@method_decorator(permission_required('permission_list'), name='dispatch')
class PermissionCreateView(View):
    def get(self, request):
        modules = Modules.objects.all()
        return render(request, 'Admin/Permissions/Permissions_List.html', {'modules': modules})
    
    def post(self, request):
        name = request.POST.get('name')
        display_name = request.POST.get('display_name')
        module_id = request.POST.get('module')
        description = request.POST.get('description')
        
        if not name or not display_name:
            messages.error(request, "Name and Display Name are required")
            return redirect('permission_list')
            
        try:
            module = Modules.objects.get(pk=module_id) if module_id else None
            Permission.objects.create(
                name=name,
                display_name=display_name,
                module=module,
                description=description
            )
            messages.success(request, "Permission created successfully")
        except Exception as e:
            messages.error(request, f"Error creating permission: {str(e)}")
        
        return redirect('permission_list')

# Permission Edit 
@method_decorator(permission_required('permission_list'), name='dispatch')
class PermissionEditView(View):
    def get(self, request, pk):
        permission = get_object_or_404(Permission.objects.select_related('module'), pk=pk)
        return JsonResponse({
            'id': permission.id,
            'name': permission.name,
            'display_name': permission.display_name,
            'module_id': permission.module.id if permission.module else None,
            'description': permission.description
        })
    
    def post(self, request, pk):
        permission = get_object_or_404(Permission, pk=pk)
        permission.name = request.POST.get('name')
        permission.display_name = request.POST.get('display_name')
        module_id = request.POST.get('module')
        permission.module = Modules.objects.get(pk=module_id) if module_id else None
        permission.description = request.POST.get('description')
        
        try:
            permission.save()
            messages.success(request, "Permission updated successfully")
        except Exception as e:
            messages.error(request, f"Error updating permission: {str(e)}")
        
        return redirect('permission_list')

# Permission Delete View
@method_decorator(permission_required('permission_list'), name='dispatch')
class PermissionDeleteView(View):
    def post(self, request, pk):
        permission = get_object_or_404(Permission, pk=pk)
        try:
            permission.delete()
            messages.success(request, "Permission deleted successfully")
        except Exception as e:
            messages.error(request, f"Error deleting permission: {str(e)}")
        
        return redirect('permission_list')

############################################################################################################################################
# Login Module
def LoginFormView(request):
    # If the user is already logged in, redirect to the dashboard
    if request.user.is_authenticated:
            # Redirect based on user role
            if request.user.role.id in [1,3]:
                return redirect('view_dashboard')  # Redirect to the dashboard if role is 1
            else:
                return redirect('view_dashboard')  # Redirect to home for any other role

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        remember_me = request.POST.get("rememberMe") == "on"
        if form.is_valid():
            login_input = form.cleaned_data.get("phone")  # This field should be renamed to "login_input" in your form
            password = form.cleaned_data.get("password")
            user = authenticate_username_email_or_phone(login_input, password)

            if user is not None:
                if user.is_active:  # Check if the user is active
                    if user.role_id in [1,3]:  # Check if user's role_id is 1
                        login(request, user)
                        if remember_me:
                            request.session.set_expiry(1209600)
                        messages.success(request, "Login Successful")
                        return redirect("view_dashboard")
                    else:
                        messages.error(
                            request,
                            "You do not have the required role to access this site.",
                        )
                else:
                    # Add error message if user account is deactivated
                    messages.error(
                        request,
                        "Your account is deactivated. Please contact the admin.",
                    )
            else:
                # Add error message for invalid credentials
                messages.error(request, "Invalid login credentials")
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, "Admin_Login.html", {"form": form})

# Authenticate username, email or phone
def authenticate_username_email_or_phone(login_input, password):
    # Try to find user by username, email, or phone
    try:
        # Check if input is numeric (could be phone)
        if login_input.isdigit():
            user = User.objects.get(phone=login_input)
        # Check if input contains @ (could be email)
        elif '@' in login_input:
            user = User.objects.get(email=login_input)
        else:
            # Otherwise treat as username
            user = User.objects.get(username=login_input)
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        # Handle case where multiple users might have the same email/phone (shouldn't happen if fields are unique)
        return None

    # Use Django's built-in authenticate to verify the password
    if user:
        user = authenticate(username=user.username, password=password)
        return user
    return None

################################ Dashboard View ##########################################
@method_decorator(permission_required('view_dashboard'), name='dispatch')
class Dashboard(LoginRequiredMixin, View):

    def get_monthly_url_stats(self):
        """Get URL stats for last 12 months by month"""
        from django.db.models.functions import TruncMonth
        
        twelve_months_ago = timezone.now() - timedelta(days=365)
        
        # Organize data for chart
        months = []
        safe_counts = []
        unsafe_counts = []
        
        # Initialize data for last 12 months
        for i in range(12):
            date = timezone.now() - timedelta(days=30*(11-i))
            months.append(date.strftime("%b %Y"))
            safe_counts.append(0)
            unsafe_counts.append(0)
        
        
        return {
            'months': months,
            'safe_counts': safe_counts,
            'unsafe_counts': unsafe_counts
        }
    
    def get(self, request, *args, **kwargs):
        
        # Get user counts by role
        role_counts = Role.objects.annotate(
            user_count=Count('user', distinct=True)
        ).values('id', 'name_en', 'user_count')
        
        
        # Total users count
        total_users = User.objects.count()
        
        # Mobile app users count (assuming role ID 1 is for mobile users)
        mobile_users = User.objects.filter(role=1).count()
        
        # Sub-admin count (assuming role ID 2 is for sub-admins)
        sub_admin_users = User.objects.filter(role=2).count()
        
        
        
        
        




        
            
        
        
        
        

        context = {
            'role_counts': role_counts,
            'total_users': total_users,
        }
        
        return render(request, "Admin/Dashboard.html", context)

############################################## Logout Module ##################################################
def logout_view(request):
    logout(request)
    return redirect("adminlogin")
################################## SytemSettings view #######################################################
@method_decorator(permission_required('System_Settings'), name='dispatch')
class System_Settings(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()  # Fetch the first record
        return render(
            request,
            "Admin/System_Settings.html",
            {
                "system_settings": system_settings,
                "MEDIA_URL": settings.MEDIA_URL,
                "breadcrumb": {
                    "parent": "Admin",
                    "child": "System Settings",
                },  # Pass MEDIA_URL to the template
            },
        )
# Handle POST request for updating system settings
    def post(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()
        if not system_settings:
            system_settings = SystemSettings()

        fs = FileSystemStorage(
            location=os.path.join(settings.MEDIA_ROOT, "System_Settings")
        )

        errors = {}
        success = False

        try:
            # Handle file uploads: Fav Icon, Footer Logo, Header Logo, and Images
            file_fields = {
                "fav_icon": "fav_icon",
                "footer_logo": "footer_logo",
                "header_logo": "header_logo",
            }

            for field_name, field_label in file_fields.items():
                if field_name in request.FILES:
                    field_file = request.FILES[field_name]
                    current_file = getattr(system_settings, field_label, None)

                    # Remove old file if it exists
                    if current_file:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, current_file)
                        if os.path.isfile(old_file_path):
                            os.remove(old_file_path)

                    # Generate a unique filename and store the file
                    file_extension = field_file.name.split(".")[-1]
                    unique_suffix = get_random_string(8)
                    file_filename = f"system_settings/{field_label}_{unique_suffix}.{file_extension}"
                    
                    # Save the file using default storage
                    image_path = default_storage.save(file_filename, field_file)
                    
                    # Update the system_settings with the new file path
                    setattr(system_settings, field_label, image_path)

            # Save changes to the system_settings model
            system_settings.save()

            # Handle other settings fields from request.POST
            settings_fields = {
                "website_name_english": "This field is required.",
                "website_name_arabic": "This field is required.",
                "phone": "This field is required.",
                "email": "This field is required.",
                "address": "This field is required.",
                "currency_symbol": "This field is required.",
            }

            for field, error_message in settings_fields.items():
                field_value = request.POST.get(field)

                if not field_value and error_message:
                    errors[field] = error_message
                else:
                    setattr(system_settings, field, field_value)


            # Check if there are any errors
            if errors:
                messages.error(request, "Please correct the errors below.")
            else:
                system_settings.save()
                success = True
                messages.success(request, "System settings updated successfully.")

        except Exception as e:
            messages.error(request, "An error occurred: {}".format(e))


        # Handle the response based on errors or success
        if errors:
            # Create a more descriptive error message listing all missing fields
            error_fields = list(errors.keys())
            if len(error_fields) == 1:
                error_msg = f"Please provide a value for the {error_fields[0]} field."
            else:
                error_msg = "Please provide values for the following fields: " + ", ".join(error_fields) + "."
            
            messages.error(request, error_msg)
            
            return render(
                request,
                "Admin/System_Settings.html",
                {
                    "system_settings": system_settings,
                    "MEDIA_URL": settings.MEDIA_URL,
                    "breadcrumb": {"parent": "Admin", "child": "System Settings"},
                    "errors": errors,
                },
            )
        elif success:
            messages.success(request, "System settings updated successfully.")
            return redirect("System_Settings")
        else:
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect("System_Settings")
        
##################################################### User Change Password View ###############################################################
def change_password_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            # Log the user out after password change
            logout(request)
            # Add a success message for the user (optional)
            messages.success(request, "Your password has been successfully updated! Please log in with your new credentials.")
            
            # Return the success response with a redirect URL
            return JsonResponse({'success': 'Your password has been successfully updated!',
                                  'redirect': '/adminlogin/'})  # Redirect to login page after password change
        else:
            errors = {}
            for field in form.errors:
                errors[field] = form.errors.get(field)
            return JsonResponse({'errors': errors})

    return JsonResponse({'error': 'Invalid request'}, status=400)

##################################################### User Profile View ###############################################################
@method_decorator(permission_required('user_profile'), name='dispatch')
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            "user": user,
            "breadcrumb": {"parent": "Acccount", "child": "Profile"},
        }

        return render(request, "Admin/User/User_Profile.html", context)

    def post(self, request):
        user = request.user

        return render(request, "Admin/User/User_Profile.html", {"user": user})


##################################################### User Update Profile View ###############################################################
@method_decorator(permission_required('user_profile'), name='dispatch')
class UserUpdateProfileView(View):
    def get(self, request, *args, **kwargs):
        form = UserUpdateProfileForm(instance=request.user)
        password_change_form = CustomPasswordChangeForm(user=request.user)
        return render(
            request,
            "Admin/User/Edit_Profile.html",
            {
                "form": form,
                "password_change_form": password_change_form,
                "breadcrumb": {"parent": "Acccount", "child": "Edit Profile"},
                "show_change_password_modal": False,
            },
        )
# Handle POST request for updating profile
    def post(self, request, *args, **kwargs):
        # Handle profile update
        user = request.user
        form = UserUpdateProfileForm(
            request.POST, instance=user, files=request.FILES
        )
        if form.is_valid():
            # Handle profile picture update
            # Initialize FileSystemStorage for profile pictures and card headers
            fs = FileSystemStorage(
                location=os.path.join(settings.MEDIA_ROOT, "profile_pics")
            )
            card_fs = FileSystemStorage(
                location=os.path.join(settings.MEDIA_ROOT, "card_header")
            )

            # Handle profile picture
            if "profile_picture" in request.FILES:
                # Remove old profile picture if it exists
                if user.profile_picture:
                    old_profile_picture_path = os.path.join(
                        settings.MEDIA_ROOT,
                        str(user.profile_picture),  # Convert to string
                    )
                    if os.path.isfile(old_profile_picture_path):
                        os.remove(old_profile_picture_path)

                # Save new profile picture
                profile_picture_file = request.FILES["profile_picture"]
                file_extension = profile_picture_file.name.split(".")[-1]
                unique_suffix = get_random_string(8)
                profile_picture_filename = (
                    f"{request.user.id}_{unique_suffix}.{file_extension}"
                )
                fs.save(profile_picture_filename, profile_picture_file)
                user.profile_picture = os.path.join(
                    "profile_pics", profile_picture_filename
                )
            elif "profile_picture-clear" in request.POST:
                # Clear the profile picture field
                if user.profile_picture:
                    old_profile_picture_path = os.path.join(
                        settings.MEDIA_ROOT,
                        str(user.profile_picture),  # Convert to string
                    )
                    if os.path.isfile(old_profile_picture_path):
                        os.remove(old_profile_picture_path)
                user.profile_picture = None

            # Handle card_header
            if "card_header" in request.FILES:
                # Remove old card header if it exists
                if user.card_header:
                    old_card_header_path = os.path.join(
                        settings.MEDIA_ROOT,
                        str(user.card_header),  # Convert to string
                    )
                    if os.path.isfile(old_card_header_path):
                        os.remove(old_card_header_path)

                # Save new card header
                card_header_file = request.FILES["card_header"]
                file_extension = card_header_file.name.split(".")[-1]
                unique_suffix = get_random_string(8)
                card_header_filename = (
                    f"card_header_{unique_suffix}.{file_extension}"
                )
                card_fs.save(card_header_filename, card_header_file)
                user.card_header = os.path.join("card_header", card_header_filename)
            elif "card_header-clear" in request.POST:
                # Clear the card header field
                if user.card_header:
                    old_card_header_path = os.path.join(
                        settings.MEDIA_ROOT,
                        str(user.card_header),  # Convert to string
                    )
                    if os.path.isfile(old_card_header_path):
                        os.remove(old_card_header_path)
                user.card_header = None

            user = form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("edit_profile")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            password_change_form = CustomPasswordChangeForm(user=request.user)
            return render(
                request,
                "Admin/User/Edit_Profile.html",
                {"form": form, "password_change_form": password_change_form},
            )

################################################################# Role CRUD Views ###################################################

# User Role List Module  
@method_decorator(permission_required('role_list'), name='dispatch')
class RoleView(LoginRequiredMixin, View):
    template_name = "Admin/Permissions/User_Role.html"

    def get(self, request):
        roles = Role.objects.all()
        return render(
            request,
            self.template_name,
            {
                "roles": roles,
                "breadcrumb": {"child": "Role List"},
            },
        )

# Role Create Views
@method_decorator(permission_required('role_list'), name='dispatch')
class RoleCreateView(LoginRequiredMixin, View):
    def post(self, request):
        name_en = request.POST.get("name_en")
        name_ar = request.POST.get("name_ar")

        if not name_en:
            messages.error(request, "English name is required.")
            return redirect("role_list")

        try:
            Role.objects.create(
                name_en=name_en,
                name_ar=name_ar,
            )
            messages.success(request, "Role added successfully.")
        except Exception as e:
            messages.error(request, f"Error creating role: {str(e)}")
        
        return redirect("role_list")

# Role Edit Views
@method_decorator(permission_required('role_list'), name='dispatch')
class RoleEditView(LoginRequiredMixin, View):
    def post(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        role.name_en = request.POST.get("name_en")
        role.name_ar = request.POST.get("name_ar")

        try:
            role.save()
            messages.success(request, "Role updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating role: {str(e)}")
        
        return redirect("role_list")

# Role Delete Views
@method_decorator(permission_required('role_list'), name='dispatch')
class RoleDeleteView(LoginRequiredMixin, View):
    def post(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        try:
            role.delete()
            messages.success(request, "Role deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting role: {str(e)}")
        return redirect("role_list")
    

############################################## List of Default User ##############################################################
@method_decorator(permission_required('default_user_list'), name='dispatch')
class DefaultUserList(LoginRequiredMixin, View):
    template_name = "Admin/User/Default_User_List.html"

    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX request for datatable data
            draw = int(request.GET.get('draw', 1))
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search[value]', '')
                        
            # Get the custom user model
            User = get_user_model()
            
            # Prepare queryset
            queryset = User.objects.filter(role_id=2)
            
            # Apply search
            if search_value:
                queryset = queryset.filter(
                    Q(username__icontains=search_value) |
                    Q(name__icontains=search_value) |
                    Q(email__icontains=search_value) |
                    Q(phone__icontains=search_value)
                )
            # Apply ordering
            queryset = queryset.order_by('name')
            # Get total count before pagination
            total_records = queryset.count()
            
            # Pagination
            paginator = Paginator(queryset, length)
            page = (start // length) + 1
            users = paginator.get_page(page)
            
            # Prepare response data
            data = []
            for i, user in enumerate(users, start=start + 1):
                data.append({
                    'id': i,
                    'username': user.username,
                    'name': user.name or '',
                    'email': user.email,
                    'phone': user.phone or '',
                    'is_active': user.is_active,
                    'actions': user.id,
                    # Additional data for forms
                    'user_id': user.id,
                    'current_status': 'activate' if user.is_active else 'deactivate'
                })
            
            response = {
                'draw': draw,
                'recordsTotal': total_records,
                'recordsFiltered': total_records,
                'data': data,
            }
            return JsonResponse(response)
        
        # Regular GET request
        roles = Role.objects.filter(id=2)
        return render(
            request,
            self.template_name,
            {
                "roles": roles,
                "breadcrumb": {"child": "Default User List"},
            },
        )
############################################## User Detail View ##############################################################
@method_decorator(permission_required('default_user_list'), name='dispatch')
class UserDetailView(LoginRequiredMixin, View):
    template_name = "Admin/User/User_Detail.html"

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Get all invoices for this user
            invoices = Invoice.objects.filter(user=user).order_by('-bill_date')
            
            # Calculate summary statistics
            invoice_stats = invoices.aggregate(
                total_invoices=Count('id'),
                total_amount=Sum('total_amount'),
                total_jugs=Sum('jug_count'),
                total_bottles=Sum('bottle_count')
            )
            
            # Handle None values from aggregation
            total_invoices = invoice_stats['total_invoices'] or 0
            total_amount = invoice_stats['total_amount'] or 0
            total_jugs = invoice_stats['total_jugs'] or 0
            total_bottles = invoice_stats['total_bottles'] or 0
            
            context = {
                "user": user,
                "title": "User Detail",
                "invoices": invoices,
                "total_invoices": total_invoices,
                "total_amount": total_amount,
                "total_jugs": total_jugs,
                "total_bottles": total_bottles,
            }
            
            return render(request, self.template_name, context)
            
        except User.DoesNotExist:
            return redirect("view_dashboard")

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Get all invoices for this user
            invoices = Invoice.objects.filter(user=user).order_by('-bill_date')
            
            # Calculate summary statistics
            invoice_stats = invoices.aggregate(
                total_invoices=Count('id'),
                total_amount=Sum('total_amount'),
                total_jugs=Sum('jug_count'),
                total_bottles=Sum('bottle_count')
            )
            
            # Handle None values from aggregation
            total_invoices = invoice_stats['total_invoices'] or 0
            total_amount = invoice_stats['total_amount'] or 0
            total_jugs = invoice_stats['total_jugs'] or 0
            total_bottles = invoice_stats['total_bottles'] or 0
            
            context = {
                "user": user,
                "title": "User Detail",
                "invoices": invoices,
                "total_invoices": total_invoices,
                "total_amount": total_amount,
                "total_jugs": total_jugs,
                "total_bottles": total_bottles,
            }
            
            return render(request, self.template_name, context)
            
        except User.DoesNotExist:
            return redirect("view_dashboard")

############################ User Active & Deactivate Function ########################################
@method_decorator(permission_required('default_user_list'), name='dispatch')
class ToggleUserStatusView(View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        requested_action = request.POST.get("status") 
        # Determine the source page based on user role
        role_redirect_map = {
            2: "default_user_list",
        }
        source_page = role_redirect_map.get(user.role_id, "view_dashboard")
        # Check if the user is a superuser (role_id == 1)
        if user.role_id == 1:
            messages.error(request, "Superuser status cannot be changed.")
            return redirect("view_dashboard")
        # Prevent self-deactivation
        if user == request.user and requested_action == "deactivate":
            messages.info(
                request, "Your account has been deactivated. Please log in again."
            )
            user.is_active = False
            user.save()
            return redirect(reverse("adminlogin"))
        # Update the user's status based on the requested action
        if requested_action == "activate":
            user.is_active = True
            messages.success(request, f"{user.username} has been activated.")
        elif requested_action == "deactivate":
            user.is_active = False
            messages.success(request, f"{user.username} has been deactivated.")
        else:
            # Fallback: toggle based on current status
            user.is_active = not user.is_active
            status_text = "activated" if user.is_active else "deactivated"
            messages.success(request, f"{user.username} has been {status_text}.")
        user.save()
        return redirect(reverse(source_page))

#################################  Modules CRUD for Permissions #######################################
@method_decorator(permission_required('module_list'), name='dispatch')
class ModuleListView(View):
    def get(self, request):
        modules = Modules.objects.all()
        return render(request, 'Admin/Permissions/Module_List.html', {
            'modules': modules,
            'breadcrumb': {'child': 'Module Management'}
        })

@method_decorator(permission_required('module_list'), name='dispatch')
class ModuleCreateView(View):
    def get(self, request):
        return render(request, 'Admin/Permissions/Module_List.html')
    
    def post(self, request):
        name_en = request.POST.get('name_en')
        name_ar = request.POST.get('name_ar')
        
        if not name_en:
            messages.error(request, "English name is required")
            return redirect('module_list')
            
        try:
            Modules.objects.create(
                name_en=name_en,
                name_ar=name_ar
            )
            messages.success(request, "Module created successfully")
        except Exception as e:
            messages.error(request, f"Error creating module: {str(e)}")
        
        return redirect('module_list')

@method_decorator(permission_required('module_list'), name='dispatch')
class ModuleEditView(View):
    def get(self, request, pk):
        module = get_object_or_404(Modules, pk=pk)
        return JsonResponse({
            'id': module.id,
            'name_en': module.name_en,
            'name_ar': module.name_ar
        })
    
    def post(self, request, pk):
        module = get_object_or_404(Modules, pk=pk)
        module.name_en = request.POST.get('name_en')
        module.name_ar = request.POST.get('name_ar')
        
        try:
            module.save()
            messages.success(request, "Module updated successfully")
        except Exception as e:
            messages.error(request, f"Error updating module: {str(e)}")
        
        return redirect('module_list')

@method_decorator(permission_required('module_list'), name='dispatch')
class ModuleDeleteView(View):
    def post(self, request, pk):
        module = get_object_or_404(Modules, pk=pk)
        try:
            module.delete()
            messages.success(request, "Module deleted successfully")
        except Exception as e:
            messages.error(request, f"Error deleting module: {str(e)}")
        
        return redirect('module_list')

@method_decorator(permission_required('customer_list'), name='dispatch')
class CustomerListView(View):
    def get(self, request):
        customers = User.objects.filter(role_id=2)  # role_id 2 is for customers
        return render(request, 'Admin/User/Customer_List.html', {
            'customers': customers,
            'breadcrumb': {'child': 'Customer Management'}
        })

@method_decorator(permission_required('customer_list'), name='dispatch')
class CustomerCreateView(View):
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')
        
        # Validate required fields
        if not all([name, phone]):
            messages.error(request, 'Name and Phone are required')
            return redirect('customer_list')
            
        # Check if phone already exists
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number is already registered')
            return redirect('customer_list')
            
        # Generate username from phone number (unique)
        username = f"cust_{phone}"
        
        try:
            # Create the customer user
            user = User.objects.create(
                name=name,
                username=username,
                phone=phone,
                address=address,
                role_id=2,  # Customer role
                is_staff=False,
                is_active=True
            )
            
            messages.success(request, 'Customer created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Customer: {str(e)}')
        
        return redirect('customer_list')

@method_decorator(permission_required('customer_list'), name='dispatch')
class CustomerEditView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, role_id=2)
        
        # Update fields
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address', '')
        
        try:
            user.save()
            messages.success(request, 'Customer updated successfully')
        except Exception as e:
            messages.error(request, f'Error updating Customer: {str(e)}')
        
        return redirect('customer_list')

@method_decorator(permission_required('customer_list'), name='dispatch')
class CustomerToggleStatusView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, role_id=2)
        user.is_active = not user.is_active
        user.save()
        
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f'Customer {status} successfully')
        return redirect('customer_list')

@method_decorator(permission_required('customer_list'), name='dispatch')
class CustomerDeleteView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, role_id=2)
        try:
            user.delete()
            messages.success(request, 'Customer deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting Customer: {str(e)}')
        
        return redirect('customer_list')

############################# Language Management ###############################
def get_language(request):
    allowed_languages = {'en', 'ar'}
    language = request.GET.get('Language', '').lower()

    if language in allowed_languages:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')
        if language not in allowed_languages:
            language = 'en'
        request.session['language'] = language

    request.session['current_language'] = language  # Keep 'current_language' consistent
    return language if language in ['en', 'ar'] else 'en'


# Send OTP for Forgot Password Email
def send_forgot_password_otp(email, otp, language, system_settings, subject, request):
    
    try:
        logo = system_settings.footer_logo if system_settings and system_settings.footer_logo else ''
        
        # Prepare context for email template
        context = {
            'otp': otp,
            'logo': logo,
        }
        
        # Choose template based on language
        template_name = f'Admin/Emails/forgot_password_otp_{language}.html'
        
        # Render email content from template
        email_content = render_to_string(template_name, context)
        
        # Send the email
        send_mail(
            subject=subject,
            message=_('Your OTP code is: %(otp)s') % {'otp': otp},  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=email_content,
            fail_silently=False,
        )
        return True
        
    except Exception as e:
        return False

# Send OTP for Sub Admin Email
class ForgotPasswordAdminView(View):
    template_name = "Admin/Forgot_Password_Admin.html"
    success_url_name = "verify_otp_admin"
    fail_url_name = "Forgot_Password_Admin"

    def get(self, request):
        language = get_language(request)
        activate(language if language in ['en', 'ar'] else 'en')
        return render(request, self.template_name, {'language': language})

    def post(self, request):
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, _("Email address is required."))
            return redirect(self.fail_url_name)

        try:
            user = User.objects.get(email=email, is_active=True, is_staff=True)
            language = user.current_language
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            system_settings = SystemSettings.objects.first()
            if not system_settings:
                messages.error(request, _("System error. Please contact support."))
                return redirect(self.fail_url_name)
            
            if language == 'ar':
                subject = 'رمز تحقق لإعادة تعيين كلمة المرور'
            else:
                subject = 'Password Reset Verification Code'

            email_sent = send_forgot_password_otp(
                email=email,
                otp=otp,
                language=language,
                system_settings=system_settings,
                subject = subject,
                request=request
            )
            if email_sent:
                request.session['reset_password_email'] = email
                messages.success(request, _("A verification code has been sent to your email."))
                return redirect(self.success_url_name)
            
            # If email failed to send
            user.otp = None
            user.otp_created_at = None
            user.save()
            messages.error(request, _("Failed to send verification email. Please try again."))
            return redirect(self.fail_url_name)
            
        except User.DoesNotExist:
            # Don't reveal whether user exists or not
            messages.error(request, _("user does not exist."))
            return redirect(self.fail_url_name)
        except Exception as e:
            messages.error(request, _("An error occurred. Please try again."))
            return redirect(self.fail_url_name)

# Verify OTP for Forgot Password Email
class VerifyOTPAdminView(View):
    template_name = "Admin/Verify_OTP_Admin_Forgot_Password.html"
    login_url_name = "reset_password_admin"  # Change this to your admin login URL name
    otp_expiry_minutes = 10  # OTP expires after 10 minutes

    def get(self, request, email=None):
        # Check if email is in session (from forgot password flow)
        email = email or request.session.get('reset_password_email')
        if not email:
            messages.error(request, _("Password reset session expired. Please start again."))
            return redirect('Forgot_Password_Admin')
        
        language = get_language(request)
        activate(language if language in ['en', 'ar'] else 'en')
        
        return render(request, self.template_name, {
            'email': email,
            'language': language,
            'partial_email': self._obfuscate_email(email)
        })

    def post(self, request):
        email = request.session.get('reset_password_email')
        if not email:
            messages.error(request, _("Session expired. Please request a new OTP."))
            return redirect('Forgot_Password_Admin')

        # Try hidden field, fallback to combining from inputs
        otp = request.POST.get('full_otp', '').strip()
        if not otp:
            otp = ''.join([request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)])

        if not otp or len(otp) != 6 or not otp.isdigit():
            messages.error(request, _("Please enter a valid 6-digit OTP."))
            return self._render_error_response(request, email)

        try:
            user = User.objects.get(
                email=email,
                is_active=True,
                is_staff=True
            )

            if (user.otp != otp or 
                not user.otp_created_at or
                (timezone.now() - user.otp_created_at).total_seconds() > self.otp_expiry_minutes * 60):
                messages.error(request, _("Invalid or expired OTP. Please request a new one."))
                request.session['reset_password_email'] = email  # Keep the email in session for retry
                return self._render_error_response(request, email)

            # OTP is valid - store verification in session
            request.session['otp_verified'] = True
            request.session['reset_user_id'] = str(user.id)
            
            # Clear the OTP after successful verification
            user.otp = None
            user.otp_created_at = None
            user.save()
            
            messages.success(request, _("OTP verified successfully. You can now reset your password."))
            return redirect(self.login_url_name)

        except User.DoesNotExist:
            messages.error(request, _("User not found. Please try again."))
            return redirect('Forgot_Password_Admin')
        except Exception as e:
            messages.error(request, _("An error occurred. Please try again."))
            return self._render_error_response(request, email)


    def _render_error_response(self, request, email):
        """Helper method to render the error response with the same context as get"""
        language = get_language(request)
        activate(language if language in ['en', 'ar'] else 'en')
        
        return render(request, self.template_name, {
            'email': email,
            'language': language,
            'partial_email': self._obfuscate_email(email)
        })

    def _obfuscate_email(self, email):
        """Helper method to partially obscure the email for display"""
        if '@' not in email:
            return email
        name, domain = email.split('@', 1)
        if len(name) > 3:
            obscured = name[:2] + '*' * (len(name)-2) + '@' + domain
        else:
            obscured = name[0] + '*' * (len(name)-1) + '@' + domain
        return obscured


class ResetPasswordAdminView(View):
    template_name = "Admin/Reset_Password_Admin.html"
    success_url_name = "adminlogin"  # URL name for admin login
    session_key = 'reset_user_id'

    def get(self, request):
        # Check if OTP was verified
        if not request.session.get('otp_verified'):
            messages.error(request, _("OTP verification required first."))
            return redirect('Forgot_Password_Admin')
            
        user_id = request.session.get(self.session_key)
        if not user_id:
            messages.error(request, _("Session expired. Please start again."))
            return redirect('Forgot_Password_Admin')

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            messages.error(request, _("User not found."))
            return redirect('Forgot_Password_Admin')

        language = get_language(request)
        activate(language if language in ['en', 'ar'] else 'en')
        
        return render(request, self.template_name, {
            'language': language
        })

    def post(self, request):
        if not request.session.get('otp_verified'):
            messages.error(request, _("OTP verification required first."))
            return redirect('Forgot_Password_Admin')

        user_id = request.session.get(self.session_key)
        if not user_id:
            messages.error(request, _("Session expired. Please start again."))
            return redirect('Forgot_Password_Admin')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic password validation
        if not password or not confirm_password:
            messages.error(request, _("Please fill in all fields."))
            return render(request, self.template_name)
            
        if password != confirm_password:
            messages.error(request, _("Passwords do not match."))
            return render(request, self.template_name)
            
        if len(password) < 8:
            messages.error(request, _("Password must be at least 8 characters."))
            return render(request, self.template_name)

        try:
            user = User.objects.get(id=user_id, is_active=True)
            user.password = make_password(password)
            user.save()
            
            # Clear session variables
            request.session.pop('otp_verified', None)
            request.session.pop(self.session_key, None)
            request.session.pop('reset_password_email', None)
            
            messages.success(request, _("Password changed successfully. Please login with your new password."))
            return redirect(self.success_url_name)
            
        except User.DoesNotExist:
            messages.error(request, _("User not found."))
            return redirect('Forgot_Password_Admin')
        except Exception as e:
            messages.error(request, _("An error occurred. Please try again."))
            return render(request, self.template_name)
