from django.db import models
from django.conf import settings
#from tinymce.models import HTMLField
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class BlogPost(models.Model):
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    title               = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    updated_on          = models.DateTimeField(auto_now= True)
    content             = models.TextField()#HTMLField()
    tag                 = TaggableManager()
    view                = models.IntegerField(default=0)
    image               = models.ImageField(upload_to='blog/')
    created_on          = models.DateTimeField(auto_now_add=True)
    status              = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={"slug":self.slug})

    def get_update_url(self):
        return reverse('blog:blog-admin-update', kwargs={"slug":self.slug})

    def get_delete_url(self):
        return reverse('blog:post-delete', kwargs={"slug":self.slug})

    def save(self, *args, **kwargs): # automatically save slug
        if not self.slug:
            self.slug = slugify(self.title)
        # self.user = self.request.user
        return super().save(*args, **kwargs)