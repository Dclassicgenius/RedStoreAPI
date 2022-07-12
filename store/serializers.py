
from asyncore import read
from .models import Product, Variation, ReviewRating, ProductGallery
from rest_framework import serializers
from category.serializers import CategorySerializer
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'
        read_only_fields = ('id',)

class ProductCreationListSerializer(serializers.ModelSerializer):
    product_name    = serializers.CharField(max_length=200, allow_blank=False)
    slug            = serializers.SlugField(max_length=200)
    description     = serializers.CharField(max_length=500, allow_blank=True)
    price           = serializers.IntegerField()
    images          = VersatileImageFieldSerializer(allow_empty_file=True, sizes=[('full_size', 'url'), ('thumbnail', 'thumbnail__100x100'),])
    stock           = serializers.IntegerField()
    is_available    = serializers.BooleanField(default=True)

    count_reviews = serializers.SerializerMethodField(read_only=True)
    average_review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'modified_date',)

        expandable_fields = {
            'category': (CategorySerializer, {'many': False}),
        }
    
    def get_count_reviews(self, obj):
        return obj.countReview

    def get_average_review(self, obj):
        return obj.averageReview


class ProductDetailSerializer(serializers.ModelSerializer):
    # get_url = serializers.HyperlinkedModelSerializer(read_only=True)
    count_reviews = serializers.SerializerMethodField(read_only=True)
    average_review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'modified_date', 'get_url', 'count_reviews', 'average_review',)

        expandable_fields = {
            'category': (CategorySerializer, {'many': False}),
        }

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.images = validated_data.get('images', instance.images)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.save()
        return instance

    # def get_get_url(self, obj):
    #     return obj.get_url

    def get_count_reviews(self, obj):
        return obj.countReview

    def get_average_review(self, obj):
        return obj.averageReview


