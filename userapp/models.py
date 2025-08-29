from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('professional', 'Professional'),
        ('customer', 'Customer'),
        ('assistant', 'Assistant'),
        ('admin', 'Admin'),
    )

    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    agreeToTerms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fname', 'lname']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-id']
    

class Department(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class Professional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    profession = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='professional_profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-id']

class Review(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        unique_together = ('professional', 'customer')

    def __str__(self):
        return f"Review by {self.customer.username} for {self.vendor.name}"