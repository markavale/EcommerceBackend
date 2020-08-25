from rest_framework import status    
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework import filters

from blog.models import BlogPost
from django.conf import settings
from blog.api.serializers import BlogPostSerializer

User = settings.AUTH_USER_MODEL


@api_view(['GET','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def blog_detail_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
        data = {}
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        blog_post.view += 1
        blog_post.save()
        serializer = BlogPostSerializer(blog_post, many=False)
        return Response(serializer.data)

    elif blog_post.author != request.user:
        return Response({'Response':"You are not the author of this blog post!"})

    elif request.method == "PUT":
        serializer = BlogPostSerializer(blog_post, data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            data['update'] = "Update successful"
            return Response(data= data)
        # else:
        #     data['failure'] = "Update failure"
        #     return Response(data= data)
        #print(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        operation = blog_post.delete()
        if operation:
            data['delete'] = "Delete successful"
        else:
            data['failure'] = "delete failed"
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data)
        

# @api_view(['PUT',]) # update
# def blog_update_view(request, slug):
#     try:
#         blog_post = BlogPost.objects.get(slug=slug)
#     except BlogPost.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "PUT":
#         serializer = BlogPostSerializer(blog_post, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data['success'] = "Update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE',]) # delete
# def blog_delete_view(request, slug):
#     try:
#         blog_post = BlogPost.objects.get(slug=slug)
#     except BlogPost.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "DELETE":
#         operation = blog_post.delete()
#         data = {}
#         if operation:
#             data['success'] = "Delete successful"
#         else:
#             data['failure'] = "delete failed"
#         return Response(data=data)

# @api_view(['POST','GET',]) # create
# def blog_create_view(request):
#     blog_post = BlogPost.objects.filter(status=1).order_by('-created_on')
#     if request.method == 'GET':
#         serializer = BlogPostSerializer(blog_post, many=True)
        #return Response(serializer.data)
    

@api_view(['GET','POST',])
@permission_classes([IsAuthenticated])
def blog_list(request):
    blog_post_list = BlogPost.objects.all().order_by('-created_on')
    if request.method == "GET":
        serializer = BlogPostSerializer(blog_post_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            data = {}
            data['success'] = "Create successful"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']