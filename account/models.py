from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .validators  import MinAgeValidator
from django.conf import settings

class User(AbstractUser,  PermissionsMixin):
    profile_pic= models.ImageField(default= "default.png", upload_to= "media/profile_pics", null= True, blank= True, )
    birth_date= models.DateField(validators= [MinAgeValidator(13)], null= True, blank= True)
    bio= models.TextField(max_length= 500, null=True, blank=True, help_text='About you.')
    phone= PhoneNumberField()
    created_date = models.DateTimeField(auto_now_add=True)
    email= models.EmailField(unique=True)
    private = models.BooleanField(default=False)
    _follows = models.ManyToManyField('User', blank=True, related_name='followed_by')
    _blocks = models.ManyToManyField('User', blank=True, related_name='blocked_by')
    
    def unfollow(self, user) -> None:
        """ Helper function to remove a user from this users following list. """
        self._follows.remove(user)

    def follow(self, user, force: bool = False) -> None:
        """ Helper function to add user to a follower list. """
        self._follows.add(user)

    @property
    def following(self) -> models.QuerySet:
        """ Returns a QuerySet of Users that this user follows. """
        return self._follows.all()

    @property
    def followers(self) -> models.QuerySet:
        """ Returns a QuerySet of Users following this user. """
        return self.followed_by.all()

    def unblock(self, user) -> None:
        """ Helper function to remove a user from this users blocked list. """
        self._blocks.remove(user)

    def block(self, user) -> None:
        """ Helper function to add user to a blocked list. """
        self._blocks.add(user)

    @property
    def blocking(self) -> models.QuerySet:
        """ Returns a QuerySet of Users that this user blocked. """
        return self._blocks.all()

    @property
    def blocked_by(self) -> models.QuerySet:
        """ Returns a QuerySet of Users blocking this user. """
        return self.blocked_by.all()

    def __str__(self):
        return  self.username

class FollowRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')

    def accept(self) -> None:
        self.requester.follow(self.to_follow)

    def reject(self) -> None:
        self.delete()

    def __str__(self) -> str:
        return f'{self.requester} -> {self.to_follow}'
