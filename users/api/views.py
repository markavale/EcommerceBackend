from rest_framework import status    
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics

from django.conf import settings
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

from users.api.serializers import RegistrationSerializer, UserPropertiesSerializer, ChangePasswordResetSerializer,UserChangePasswordResetSerializer
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

@api_view(['POST'])
@permission_classes([IsAuthenticated|ReadOnly, ])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()    
            data['response'] = "Successfully registered a new user."
            data['email'] = user.email
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            token = Token.objects.get(user=user) # to get the token that has been generated
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data=data)

@api_view(['GET', 'PUT', ])
@permission_classes([IsAuthenticated, ])
def user_properties_view(request):
    try:
        user = request.user

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserPropertiesSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserPropertiesSerializer(user, data= request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'User update success'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', ])
# @permission_classes([IsAuthenticated, ])
# def update_user_view(request):
#     try:
#         user = request.user

#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "PUT":
#         serializer = UserPropertiesSerializer(user, data= request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data['response'] = 'User update success'
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(generics.UpdateAPIView):

    serializer_class = ChangePasswordResetSerializer#UserChangePasswordResetSerializer
    model = User
    permission_classes = (IsAuthenticated, )
    #authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_object(self, queryset = None):
        obj = self.request.user
        return obj

    def update(self,request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password":"Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [],
                'success-url': reverse('user:login', request=request)   
            }
            return Response(response)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
