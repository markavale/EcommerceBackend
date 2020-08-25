from rest_framework import serializers
from .models import (GraphicDesign, LightroomPreset,LightroomPresetCategory,
        LightroomPackage
    )

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)    

# class TagSerializer(serializers.RelatedField): # for nested fields

#      def to_representation(self, value):
#          return value.name

#      class Meta:
#         model = GraphicDesign.tags

class TagsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = GraphicDesign.tags
        fields = '__all__'

    def to_representation(self, value):
         return value.name


class TagsField(serializers.Field):
    def to_representation(self, value):
        """ in drf this method is called to convert a custom datatype into a primitive,
        serializable datatype.

        In this context, value is a plain django queryset containing a list of strings.
        This queryset is obtained thanks to get_tags() method on the Task model.

        Drf is able to serialize a queryset, hence we simply return it without doing nothing.
        """
        return value

    def to_internal_value(self, data):
        """ this method is called to restore a primitive datatype into its internal
        python representation.

        This method should raise a serializers.ValidationError if the data is invalid.
        """
        return data

class GraphicDesignSerializer(TaggitSerializer,serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField('get_username_from_admin')

    tags = TagListSerializerField()
    # def create(self, validated_data):
    #     # using "source=get_tags" drf "thinks" get_tags is a real field name, so the
    #     # return value of to_internal_value() is used a the value of a key called "get_tags" inside validated_data dict. We need to remove it and handle the tags manually.
    #     #tags = validated_data
    #     tag = self.tags
    #     design = GraphicDesign.objects.create(**validated_data)
    #     design.tags.add(*tag)

    #     return design
        
    class Meta:
        model = GraphicDesign
        fields = ('__all__'
        )
        extra_kwargs = {
            'downloads':{'read_only':True},
            'views':{'read_only':True},
            'slug':{'read_only':True},
            'user':{'read_only':True},
        }
    
    def get_username_from_admin(self,designs):
            username = designs.user.username
            return username

    # def save(self):
    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         user = request.user


class DesignDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphicDesign
        fields = ('__all__'
        )
        extra_kwargs = {
            'downloads':{'read_only':True},
            'views':{'read_only':True},
            'slug':{'read_only':True},
            'user':{'read_only':True},
        }


class LightroomPresetSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_admin')
    category_name = serializers.SerializerMethodField('get_category_name')
    preset_file = serializers.SerializerMethodField('get_preset_name')
    class Meta:
        model  = LightroomPreset
        fields = ('__all__')
        extra_kwargs = {
            'created_at':{'read_only':True},
            'downloads':{'read_only':True},
            'user':{'read_only':True},
        }

    def get_username_from_admin(self,preset):
            username = preset.user.username
            return username

    def get_category_name(self, preset):
        category = preset.category.category_name
        return category

    def get_preset_name(self, preset):
        preset_name = preset.get_preset_name()
        return preset_name

class LightroomPresetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LightroomPresetCategory
        fields = ('__all__')


class LightroomPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightroomPackage
        fields = ('__all__')