from django.contrib import admin
from .models import (GraphicDesign, LightroomPreset,
    LightroomPresetCategory, LightroomPackage, Order, Coupon
)


# class WebDevelopmentAdmin(admin.ModelAdmin):
    # list_fields = ['user', 'img', 'description', 'gear', 'created_at', 'updated_at']
    # ordering = ['created_at']
    

# class VideographyADmin(admin.ModelAdmin):
#     list_fields = ['user', 'description', 'gear', 'created_at', 'updated_at']
#     ordering = ['created_at']
    

# class PhotographyAdmin(admin.ModelAdmin):
#     list_fields = ['user', 'img', 'description', 'gear', 'created_at', 'updated_at']
#     ordering = ['created_at']

class GraphicDesignAdmin(admin.ModelAdmin):
    list_display = ['user', 'img','price','discount_price','slug',
                    'free', 'description', 'created_at', 'updated_at']
    ordering = ['created_at']
    prepopulated_fields = {'slug': ('title',)} # new

class LightroomPresetAdmin(admin.ModelAdmin):
    list_fields = ['user', 'title', 'slug', 'description', 'number_of_downloads']
    prepopulated_fields = {'slug': ('title',)} # new
    #ordering = ['timestamp'] 

# class LightroomPackageAdmin(admin.ModelAdmin):
#     list_fields = ['presets', 'categories']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['photoshop_items','lightroom_items','start_date',
        'ordered_date','coupon']
    ordering = ['-start_date']
    

# admin.site.register(WebDevelopment, WebDevelopmentAdmin)
# admin.site.register(Videography, VideographyADmin)
# admin.site.register(Photography, PhotographyAdmin)
admin.site.register(GraphicDesign, GraphicDesignAdmin)
admin.site.register(LightroomPreset, LightroomPresetAdmin)
admin.site.register(LightroomPresetCategory)
admin.site.register(LightroomPackage)
admin.site.register(Order,OrderAdmin)
admin.site.register(Coupon)
