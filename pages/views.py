from rest_framework import status    
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from django.contrib.auth.mixins import LoginRequiredMixin


from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer

from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = None


class IndexView(ObjectMultipleModelAPIView):
    permission_classes = ([IsAuthenticated|ReadOnly,])
    pagination_class = LimitPagination
    querylist = [
        {
            'queryset':BlogPost.objects.filter(status=1).order_by('-created_on')[0:3],
            'serializer_class':BlogPostSerializer
        },
    ]
