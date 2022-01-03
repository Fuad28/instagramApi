from django.db import models
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

class Post(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', )
    caption= models.TextField(blank= True, null= True, max_length= 1000)
    date_posted= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username + "_post"



class Images(models.Model):
    img= models.ImageField(upload_to= "media/post_imgs", default= "default.png",  null= False, blank= False)
    post= models.ForeignKey(Post, on_delete= models.CASCADE, related_name= "images")

    def __str__(self):
        return str(self.post) + "_img"

    def save(self, *args, **kwargs) -> None:
        """ To ensure a post has an image and the images are less than 5 """

        if self.post.images.count() >= 5:
            raise SuspiciousOperation('Post already contains 5 images.')
        else:
            super().save(*args, **kwargs)



