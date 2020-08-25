from django.contrib import admin
from .models import BlogPost

class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'slug', 'view','status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

        
admin.site.register(BlogPost, PostAdmin)