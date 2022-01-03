from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .validators  import MinAgeValidator

class User(AbstractUser,  PermissionsMixin):
    profile_pic= models.ImageField(default= "default.png", upload_to= "media/profile_pics", null= True, blank= True, )
    email= models.EmailField(unique=True)
    bio= models.TextField(max_length= 500, null=True, blank=True, help_text='About you.')
    private = models.BooleanField(default=True)
    phone= models.CharField(max_length=20,  default= 0)
    birth_date= models.DateField(validators= [MinAgeValidator(13)], null= True, blank= True)

    def __str__(self):
        return  self.username
