from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


#Model_user

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)


    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # we change the username because we wnat to login with our email, requied_field will be username because we replaced the unsername by email
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
        user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)
        address_line = models.CharField(max_length=100, blank=True, null=True)
        profile_picture = models.ImageField(upload_to='userprofile', blank=True, null=True)
        city = models.CharField(max_length=15, blank=True, null=True)
        #address = models.CharField(max_length=250, blank=True, null=True)
        #country = models.CharField(max_length=15, blank=True, null=True)
        #state = models.CharField(max_length=15, blank=True, null=True)
        #pin_code = models.CharField(max_length=10, blank=True, null=True)
        #latitude = models.CharField(max_length=20, blank=True, null=True)
        #longitude = models.CharField(max_length=20, blank=True, null=True)
        #location = gismodels.PointField(blank=True, null=True, srid=4326)
        created_at = models.DateTimeField(auto_now_add=True)
        modified_at = models.DateTimeField(auto_now=True)
        def __str__(self):
            return self.user.first_name
