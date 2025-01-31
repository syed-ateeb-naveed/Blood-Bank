from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from datetime import date

class UserManager(BaseUserManager):
    """
    Custom manager for User model with methods to create regular users and superusers.
    """
    def create_user(self, email, password=None, **kwargs):
        """
        Create and return a `User` with an email and password.
        """
        if email is None:
            raise TypeError("Users must have an email.")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that includes additional fields and custom user manager.
    """
    # Primary key, auto-incrementing integer ID
    id = models.AutoField(primary_key=True)

    # Timestamp when the user was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the user was last modified
    modified_at = models.DateTimeField(auto_now=True)

    # User's first name
    first_name = models.CharField(max_length=255)

    # User's last name
    last_name = models.CharField(max_length=255)

    # Optional image field for profile picture
    pic = models.ImageField(upload_to="user_pic/", blank=True, null=True)

    # Optional field for user's date of birth
    date_of_birth = models.DateField(blank=True, null=True)

    # User's email address, must be unique and indexed
    email = models.EmailField(db_index=True, unique=True)

    # Optional field for phone number
    # phone = models.CharField(max_length=15, blank=True)

    # Optional field for a user biography
    blood_group = models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, blank=True, null=True)

    # Boolean field to determine if the user's email address has been verified
    # is_verified = models.BooleanField(default=False)

    # Boolean field to determine if the user's account is active
    is_active = models.BooleanField(default=True)

    # Boolean field to determine if the user has staff permissions
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Field used for authentication
    objects = UserManager()  # Custom manager for the User model


    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def __str__(self):
        """
        Return the string representation of the User.
        """
        return self.email

    class Meta:
        verbose_name = "User"  # Singular name for the model
        verbose_name_plural = "Users"  # Plural name for the model



