from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .validators  import MinAgeValidator
from django.conf import settings

class User(AbstractUser,  PermissionsMixin):
    profile_pic= models.ImageField(default= "default.png", upload_to= "media/profile_pics", null= True, blank= True, )
    birth_date= models.DateField(validators= [MinAgeValidator(13)], null= True, blank= True)
    bio= models.TextField(max_length= 500, null=True, blank=True, help_text='About you.')
    phone= models.CharField(max_length=20, default= 0)
    private = models.BooleanField(default=True)
    email= models.EmailField(unique=True)
    
    def __str__(self):
        return  self.username

class FollowRelations(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follow_relations')
    following= models.ManyToManyField("self", blank=True, symmetrical= False, related_name='user_following')
    followers= models.ManyToManyField("self", blank=True, symmetrical= False, related_name='user_followers')
    pending= models.ManyToManyField("self", blank=True, symmetrical= False, related_name='user_pending')
    blocked= models.ManyToManyField("self",blank=True,related_name='user_blocked',symmetrical=False)
    created_date = models.DateTimeField(auto_now_add=True)
