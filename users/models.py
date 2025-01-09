from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,name, phone_number, gender='M',password=None,confirm_password=None):
        if not email:
            raise ValueError("User must have an Email")
        
        if not password:
            raise ValueError("User must have a Password")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            gender = gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,name, phone_number, email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    gender_choice = [('M','Male'),('F','Female'),('O','Others')]
    gender = models.CharField(max_length=1, choices=gender_choice, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ["name","password","phone_number",]
    
    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image_1 = models.BinaryField(null=True, blank=True)
    image_2 = models.BinaryField(null=True, blank=True)
    image_3 = models.BinaryField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
