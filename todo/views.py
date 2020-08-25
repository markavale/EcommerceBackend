from django.shortcuts import render
from rest_framework import generics, viewsets, status
# from rest_framework.status import status
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .permissions import AllowAny

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('completed', '-timestamp')
    serializer_class = TodoSerializer
    permission_classes = [AllowAny, ]
    pagination_class = PageNumberPagination

    

    
