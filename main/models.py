from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    

class BlogPost(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField() 
    image = models.ImageField(upload_to='static/blog_image/') 
    author = models.CharField(max_length=255, null=True, blank=True) 

    def __str__(self):
        return self.title