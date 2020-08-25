from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAdminUser, IsAuthenticated, #BasePermission, SAFE_METHODS,
                IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import (GraphicDesign, LightroomPreset,LightroomPresetCategory,
            LightroomPackage, Order, Coupon
    )       
from . serializers import (GraphicDesignSerializer,LightroomPresetSerializer, LightroomPresetCategorySerializer,
                LightroomPackageSerializer) 
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrReadOnly, ReadOnly

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator 

@api_view(['POST', ])
def add_to_cart(request, slug):
    photoshop_items = get_object_or_404(GraphicDesign, slug=slug)
    lightroom_items = get_object_or_404(LightroomPreset, slug=slug)
    if photoshop_items & lightroom_items:
        order_item, created = Order.objects.get_or_create(
        
        )
    else:
        if photoshop_items:
            order_item, created = Order.objects.get_or_create(
        
            )
        else:
            order_item, created = Order.objects.get_or_create(
        
            )




# Create your views here.
@method_decorator([login_required, ], name='dispatch')
class GraphicDesignsCreate(generics.CreateAPIView):
    queryset = GraphicDesign.objects.all()
    serializer_class = GraphicDesignSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class GraphicDesignsList(generics.ListAPIView):
    queryset = GraphicDesign.objects.all()
    serializer_class = GraphicDesignSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination


@method_decorator([login_required, ], name='dispatch')
class GraphicDesignsListCreate(generics.ListCreateAPIView):
    """
    A simple ViewSet for viewing and editing designs.
    """
    #lookup_field = 'slug'reverse
    pagination_class = PageNumberPagination
    queryset = GraphicDesign.objects.all().order_by('-created_at')
    serializer_class = GraphicDesignSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#@method_decorator([login_required, ], name='dispatch')
class GraphicDesignDetail(generics.RetrieveUpdateDestroyAPIView):

    #parser_classes = [MultiPartParser, FormParser]
    serializer_class = GraphicDesignSerializer
    queryset = GraphicDesign.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    #lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
        
    def get(self, request, *args, **kwargs):
        obj = GraphicDesign.objects.get(slug=kwargs['slug'])
        obj.views +=1
        obj.save()
        serializer = GraphicDesignSerializer(obj,many=False).data
        return Response(serializer)

    # def put(self, request, *args ,**kwargs):
    #     obj = GraphicDesign.objects.get(slug=kwargs['slug'])
    #     serializer = GraphicDesignSerializer(obj, data = request.data, file= request.file)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         data = {}
    #         data['response'] = 'Update success'
    #         return Response(data=data)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#@method_decorator([login_required, ], name='dispatch')
class LightroomPresetCreate(generics.CreateAPIView):
    #queryset = LightroomPreset.objects.all().order_by('-created_at')
    serializer_class = LightroomPresetSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    #pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#@method_decorator([login_required, ], name='dispatch')
class LightroomPresetList(generics.ListAPIView):
    queryset = LightroomPreset.objects.all().order_by('-created_at')
    serializer_class = LightroomPresetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    
    
#@method_decorator([login_required, ], name='dispatch')
class LightroomPresetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LightroomPreset.objects.all().order_by('-created_at')
    serializer_class = LightroomPresetSerializer
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

@method_decorator([login_required, ], name='dispatch')
class LightroomPresetCategoryList(generics.ListAPIView):
    queryset = LightroomPresetCategory.objects.all()
    serializer_class = LightroomPresetCategorySerializer
    permission_classes = [IsAdminUser]
    #lookup_field = 'id'


@method_decorator([login_required, ], name='dispatch')
class LightroomPackageList(generics.ListAPIView):
    queryset = LightroomPackage.objects.all()
    serializer_class = LightroomPackageSerializer
    permission_classes = [IsAdminUser]
    #lookup_field = 'id'