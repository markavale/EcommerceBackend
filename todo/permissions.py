from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator 
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "Error!!"
    my_safe_method = ['DELETE', 'PUT', 'GET']
    def has_object_permission(self, request, view, obj):
        if request.method in my_safe_method:
            return True
        return obj.user == request.user
        #return super().has_object_permission(request, view, obj)

class AllowAny(BasePermission):
    my_safe_method = ['DELETE', 'PUT', 'GET', 'POST'] 
    def has_permission(self, request, view):
        return request.method in self.my_safe_method


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS