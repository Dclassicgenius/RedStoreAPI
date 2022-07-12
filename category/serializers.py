from .models import Category
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'name',]

class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=50, allow_blank=False)
    slug = serializers.SlugField(max_length=100)
    description = serializers.CharField(max_length=255, allow_blank=True)
    cat_image = serializers.ImageField(allow_empty_file=True)
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'slug', 'description', 'cat_image')
        read_only_fields = ('id',)

    def validate(self, attrs):
        category_name = Category.objects.filter(category_name=attrs['category_name']).exists()
        if category_name:
            raise serializers.ValidationError('Category name exists')
        return super().validate(attrs)


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.cat_image = validated_data.get('cat_image', instance.cat_image)
        instance.save()
        return instance

    