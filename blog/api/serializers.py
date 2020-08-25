from rest_framework import serializers
from blog.models import BlogPost


class TagSerializer(serializers.RelatedField): # for nested fields

     def to_representation(self, value):
         return value.name

     class Meta:
        model = BlogPost.tag

class BlogPostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = BlogPost
        fields = ('title','updated_on','content','tag',
            'view','image','updated_on','created_on','username')

    def get_username_from_author(self,blog_post):
        username = blog_post.author.username
        return username