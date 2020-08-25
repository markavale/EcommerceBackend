from django.db import models
from django.urls import reverse
from django.shortcuts import HttpResponse
#from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify # new
import os

User = settings.AUTH_USER_MODEL

# VIDEOGRAPHY = [
#     ('Fingerstyle Acoustic Cover', 'Fingerstyle Acoustic Cover'),
#     ('Travel Highlights', 'Travel Highlights')
# ]

# TYPE=[
#     ('Web Development', 'Web Development'),
#     #('')
# ]

DESIGN = [
    ('Vector','Vector'),
    ('Art','Art'),
    ('Designs','Designs'),
    ('Photo Manipulation', 'Photo Manipulation')
]
# PHOTOGRAPHY = [
#     ('Nature', 'Nature'),
#     ('Fashion', 'Fashion'),
#     ('Aesthetic', 'Aesthetic'),
#     ('Food', 'Food')
# ]

# class WebDevelopment(models.Model):
    # user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    # title                   = models.CharField(max_length=100, blank=False, null=False)
    # filter_by               = models.CharField(max_length=100, choices=TYPE)
    # img                     = models.ImageField(blank=False, null=False, upload_to='web_development')
    # description             = models.TextField(max_length=500, blank=True, null=True)
    # url                     = models.CharField(max_length=255, blank=True, null=True)
    # tools                   = HTMLField()
    # tags                    = TaggableManager()
    # views                   = models.IntegerField(default=0)
    # created_at              = models.DateTimeField(auto_now_add=True)
    # updated_at              = models.DateTimeField(auto_now=True)

    
    # def __str__(self):
    #     return self.user.username

    # def get_absolute_url(self):
    #     return reverse("webdev-detail", kwargs={"id":self.id})

    # def get_update_url(self):
    #     return reverse("webdev-update", kwargs={"id":self.id})
    
    # def get_delete_url(self):
    #     return reverse("webdev-delete", kwargs={"id":self.id})
    
    # def last_upload(self):
    #     upload = self.WebDevelopment.objects.all()[-1]
    #     latest = upload.created_at
    #     return latest


class GraphicDesign(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=100, unique=True)
    slug                    = models.SlugField(max_length=200, unique=True)
    filter_by               = models.CharField(choices=DESIGN, max_length=100)
    img                     = models.ImageField(upload_to='graphic_design')
    description             = models.TextField(max_length=1000, blank=True, null=True)
    template                = models.FileField(upload_to='graphic_design/zip_files', blank=True, null=True)
    price                   = models.IntegerField(default=0, blank=True, null=True)
    discount_price          = models.IntegerField(blank=True, null=True)
    free                    = models.BooleanField(blank=False, null=False)
    downloads               = models.IntegerField(default=0)
    views                   = models.IntegerField(default=0)
    tags                    = TaggableManager()
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("graphic-detail", kwargs={"id":self.id})

    def get_update_url(self):
        return reverse("graphic-update", kwargs={"id":self.id})
    
    def get_delete_url(self):
        return reverse("graphic-delete", kwargs={"id":self.id})

    def get_template_name(self):
        return self.template.name.split('/')[-1]

    def get_total_price(self):
        discount = self.discount_price
        total = 0
        if not self.free:
            if discount:
                total += discount
            else:
                total += self.price
            return total

    def get_total_downloads(self):
        return self.downloads

    def get_tags(self):
        """ names() is a django-taggit method, returning a ValuesListQuerySet 
        (basically just an iterable) containing the name of each tag as a string
        """
        return self.tags.names()

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


# class Photography(models.Model):
    # user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    # title                   = models.CharField(max_length=100, blank=False, null=False)
    # img                     = models.ImageField(blank=False, null=False, upload_to='photography')
    # filter_by               = models.CharField(max_length=100, choices=PHOTOGRAPHY)
    # description             = models.TextField(max_length=150, blank=True, null=True)
    # gear                    = HTMLField()
    # tags                    = TaggableManager()
    # views                   = models.IntegerField(default=0)
    # created_at              = models.DateTimeField(auto_now_add=True)
    # updated_at              = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name_plural = 'Photographies'

    # def __str__(self):
    #     return self.user.username

    # def get_absolute_url(self):
    #     return reverse("photography-detail", kwargs={"id":self.id})

    # def get_update_url(self):
    #     return reverse("photography-update", kwargs={"id":self.id})
    
    # def get_delete_url(self):
    #     return reverse("photography-delete", kwargs={"id":self.id})



# class Videography(models.Model):
    # user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    # title                   = models.CharField(max_length=100, blank=False, null=False)
    # img                     = models.ImageField(blank=False, null=False, upload_to='videography')
    # filter_by               = models.CharField(max_length=100, choices=VIDEOGRAPHY)
    # url                     = models.CharField(max_length=255, blank=False, null=False)
    # description             = models.TextField(max_length=150, blank=True, null=True)
    # gear                    = HTMLField()
    # tags                    = TaggableManager()
    # views                   = models.IntegerField(default=0)
    # created_at              = models.DateTimeField(auto_now_add=True)
    # updated_at              = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name_plural = 'Videographies'

    # def __str__(self):
    #     return self.user.username

    # def get_absolute_url(self):
    #     return reverse("videography-detail", kwargs={"id":self.id})

    # def get_update_url(self):
    #     return reverse("videography-update", kwargs={"id":self.id})
    
    # def get_delete_url(self):
    #     return reverse("videography-delete", kwargs={"id":self.id})


class LightroomPreset(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    title               = models.CharField(max_length=100, blank=False, null=False)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(max_length=1000, blank=True, null=True)
    old_img             = models.ImageField(upload_to='lightroom')
    new_img             = models.ImageField(upload_to='lightroom')
    price               = models.IntegerField(default=0, blank=True, null=True)
    discount_price      = models.IntegerField(blank=True, null=True)
    free                = models.BooleanField(blank=False, null=False)
    preset_file         = models.FileField(upload_to='lightroom/preset')
    downloads           = models.IntegerField(default=0)
    category            = models.ForeignKey('LightroomPresetCategory',on_delete=models.CASCADE,related_name='lightroom_category')
    created_at          = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("preset-detail", kwargs={"pk": self.pk})

    def get_total_price(self):
        total = 0
        discount = self.discount_price
        if not self.free:
            if discount:
                total += discount
            else:
                total += self.price
            return total

    def get_update_url(self):
        return reverse("lightroom-update", kwargs={'id':self.id})

    def get_delete_url(self):
        return reverse("lightroom-delete", kwargs={"id":self.id})

    def get_preset_name(self):
        return self.preset_file.name.split('/')[-1]


    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class LightroomPresetCategory(models.Model):
    category_name = models.CharField(max_length=255, blank=False, null=False)
    featured_image = models.ImageField(upload_to='featured_image',default='featured_image/default.jpg')
    
    class Meta:
        verbose_name_plural = 'Lightroom preset catergories'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("preset-detail", kwargs={"pk": self.pk})

    def get_featured_image(self):
        image = self.featured_image
        if image and hasattr(image, 'url'):
            return image.url
        else:
            return '/media/lightroom/featured_image/default.jpg'
    

class LightroomPackage(models.Model):
    presets = models.ForeignKey(LightroomPreset, on_delete=models.CASCADE)
    categories = models.ForeignKey(LightroomPresetCategory, on_delete=models.CASCADE)

    def __str__(self):
        category_name = self.presets.category.category_name
        return "{} {}".format(category_name, self.presets.title)

    # def get_absolute_url(self):
    #     return reverse("preset-detail", kwargs={"pk": self.pk})

    def get_total_preset(self):
        cat_preset = self.presets.category
        total = LightroomPreset.objects.filter(category=cat_preset).count()
        return total

    def get_total_download(self):
        return self.presets.downloads

    def get_featured_image(self):
        image = self.categories.featured_image
        if image and hasattr(image, 'url'):
            return image.url
        else:
            return '/media/default.jpg'

    def get_category_name(self):
        return self.presets.category.category_name

class Coupon(models.Model):
    code    = models.CharField(max_length=15)
    amount  = models.FloatField()

    def __str__(self):
        return self.code   
    
class Order(models.Model):
    #email		            = models.EmailField(max_length = 255,null=False,blank=False, unique=True)
    photoshop_items         = models.ForeignKey(GraphicDesign, on_delete=models.CASCADE, related_name='photoshop_items', blank=True)
    lightroom_items         = models.ForeignKey(LightroomPreset, on_delete=models.CASCADE, related_name='lightroom_items', blank=True)
    start_date              = models.DateTimeField(auto_now_add=True)
    ordered_date            = models.DateTimeField()
    coupon                  = models.ForeignKey('Coupon', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email

    def get_total(self):
        total = 0
        for order_item in self.photoshop_items.all():
            total += order_item.get_total_price()
        for order_item in self.lightroom_items.all():
            total += order_item.get_total_price()
        if self.coupon:    
            total -= self.coupon.amount
        return total

