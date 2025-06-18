from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime 
from decimal import Decimal
from num2words import num2words






class Modules(models.Model):
    name_en = models.CharField(max_length=100, null=True, blank=True)
    name_ar = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name_en
    
    class Meta:
        db_table = 'invoice_modules'
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)  # e.g., "create_user", "edit_role"
    display_name = models.CharField(max_length=255, null=True, blank=True)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.module.name_en if self.module else 'No Module'} - {self.display_name or self.name}"
    
    class Meta:
        db_table = 'invoice_permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['module__name_en', 'display_name']

# Role Model
class Role(models.Model):
    name_en = models.CharField(max_length=100,null=True,blank=True)
    name_ar = models.CharField(max_length=100,null=True,blank=True)
    permissions = models.ManyToManyField(
        Permission,
        through='RoleHasPermission',
        through_fields=('role', 'permission'),
        related_name='roles'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 

    def __str__(self):
        return self.name_en
    class Meta:
        db_table = 'invoice_role'

# Role Has Permission Model (junction table)
class RoleHasPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoice_role_has_permissions'
        unique_together = ('role', 'permission')
    
    class Meta:
        db_table = 'invoice_role_has_permissions'



# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)

              

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
    def __str__(self):
        return self.username
    
    def has_permission(self, permission_name):
        if self.is_superuser:
            return True
        return self.role.permissions.filter(name=permission_name).exists()
    
    def has_any_permission(self, permission_names):
        if self.is_superuser:
            return True
        return self.role.permissions.filter(name__in=permission_names).exists()

    class Meta:
        db_table = 'invoice_user'


# System Settings Model
class SystemSettings(models.Model):
    fav_icon = models.CharField(max_length=255, null=True, blank=True)
    header_logo = models.CharField(max_length=255, null=True, blank=True)
    website_name_english = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    currency_symbol = models.CharField(max_length=10,null=True, blank=True)    
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.website_name_english
    
    class Meta:
        db_table = 'invoice_systemsettings'


class Invoice(models.Model):
    BILL_TEMPLATE_CHOICES = [
        ('1', 'હરેશ એ પટેલ'),
        ('2', 'ખોડલ વોટર સપ્લાયર્સ'),
        ('3', 'ભાવેશ આર શાહ'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Assuming User model exists
    bill_template = models.CharField(max_length=10, choices=BILL_TEMPLATE_CHOICES)
    bill_number = models.CharField(max_length=100, unique=True, blank=True)
    bill_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Jug fields
    jug = models.IntegerField(default=0)  # For backward compatibility
    jug_count = models.IntegerField(default=0)
    jug_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('25.00'))
    
    # Bottle fields
    bottle = models.IntegerField(default=0)  # For backward compatibility
    bottle_count = models.IntegerField(default=0)
    bottle_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('25.00'))
    
    # Other charges
    other = models.CharField(max_length=255, null=True, blank=True)
    other_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Total amount
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Timestamps
    bill_created_at = models.DateTimeField(auto_now_add=True)
    bill_updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def number_to_words(number):
        """Convert number to words"""
        try:
            return num2words(float(number), lang='en').title() + " Only"
        except:
            return "Zero Only"

    @property
    def jug_total(self):
        """Calculate jug total amount"""
        return Decimal(str(self.jug_count)) * self.jug_amount

    @property
    def bottle_total(self):
        """Calculate bottle total amount"""
        return Decimal(str(self.bottle_count)) * self.bottle_amount

    @property
    def total_amount_in_words(self):
        """Get total amount in words"""
        return self.number_to_words(self.total_amount)

    @classmethod
    def generate_bill_number(cls):
        """Generate unique bill number"""
        current_year = timezone.now().year
        # Get the last invoice for the current year
        last_invoice = cls.objects.filter(
            bill_number__startswith=str(current_year)
        ).order_by('-bill_number').first()
        
        if last_invoice:
            try:
                # Extract the sequence number from the last bill number
                last_number = int(last_invoice.bill_number[-4:])
            except (ValueError, IndexError):
                last_number = 0
        else:
            last_number = 0
        
        new_number = last_number + 1
        return f"{current_year}{new_number:04d}"

    def save(self, *args, **kwargs):
        """Override save method to auto-generate bill number and calculate totals"""
        # Generate bill number if not exists
        if not self.bill_number:
            self.bill_number = self.generate_bill_number()
        
        # Calculate total amount
        self.total_amount = self.jug_total + self.bottle_total + self.other_amount
        
        # Set bill_amount to match total_amount
        self.bill_amount = self.total_amount
        
        # Sync jug and bottle fields for backward compatibility
        self.jug = self.jug_count
        self.bottle = self.bottle_count
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill_number} - {self.user.name if hasattr(self.user, 'name') else self.user.username}"

    class Meta:
        db_table = 'invoice_invoice'
        ordering = ['-bill_date', '-bill_created_at']