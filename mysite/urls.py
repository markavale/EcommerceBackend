from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blog/', include('blog.api.urls', namespace='blog')),
    path('api/user/', include('users.api.urls', namespace='user')),
    path('api/', include('pages.urls', namespace='pages')),
    path('api/shop/', include('shop.urls', namespace='shop')),
    path('api/', include('marketing.urls', namespace='marketing')),
    path('api/', include('todo.urls', namespace='todo')),

    #3rd party
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)