from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from courses.models import Course

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_superuser(provide,email,password,name,**otherData):
        otherData.setdefault('is_staff',True)
        otherData.setdefault('is_superuser',True)

        if otherData.get('is_staff') != True:
         return ValueError("Administrator moet is_staff value hebben")
        
        if otherData.get('is_superuser') != True:
         return ValueError("Administrator moet is_superuser value hebben")
    
        return provide.create_user(email,password,name,**otherData)


    def create_user(provide,email,password,name,**otherData):
        if not email:
         raise ValueError("U moet een geldige e-mail adres bijgeven")
        email=provide.normalize_email(email)
        user=provide.model(email=email,name=name,**otherData)
        user.set_password(password) #hashen onze password
        user.save() # sla hashed value op in SQLite
        return user



class User(AbstractBaseUser, PermissionsMixin):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255, unique = True)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    is_staff=models.BooleanField(default=False)
    courseActivated=models.ManyToManyField(Course)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    #objects = obj
    objects=UserManager()

    def __str__(provide):
        return provide.name + " " + provide.email


    def capture_all_courses(provide):
        courses = []
        for x in provide.courseActivated.all():
            courses.append(x.courseUUID)