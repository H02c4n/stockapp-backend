from rest_framework import serializers
from .models import Category, Firm, Brand, Sales, Product, Purchases
import datetime

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id','name', 'product_count')

    def get_product_count(self, obj):
        return Product.objects.filter(category_id = obj.id).count()





class ProductSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'category_id',
            'brand',
            'brand_id',
            'stock'
        )
        read_only_fields =('stock',)





class CategoryProductSerializer(serializers.ModelSerializer):

    products = ProductSerializer(many=True)
    product_count= serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count', 'products')

    def get_product_count(self, obj):
        return Product.objects.filter(category_id = obj.id).count()


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ('id', 'name', 'image')



class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id',
            'name',
            'phone',
            'image',
            'address'
        )




class PurchasesSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    time_hour = serializers.SerializerMethodField()
    createds = serializers.SerializerMethodField()
    class Meta:
        model = Purchases
        fields = (
            'id',
            'user',
            'firm_id',
            'firm',
            'brand_id',
            'brand',
            'category',
            'product_id',
            'product',
            'quantity',
            'price',
            'price_total',
            'createds',
            'time_hour',
        )


    def get_category(self, obj):
        return obj.product.category.name


    def get_time_hour(self, obj):
        return datetime.datetime.strftime(obj.createds, "%H:%M")
    

    def get_createds(self, obj):
        return datetime.datetime.strftime(obj.createds, "%d,%m,%Y")





class SalesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    time_hour = serializers.SerializerMethodField()
    createds = serializers.SerializerMethodField()
    class Meta:
        model = Sales
        fields = (
            'id',
            'user',
            'brand_id',
            'brand',
            'category',
            'product_id',
            'product',
            'quantity',
            'price',
            'price_total',
            'createds',
            'time_hour',
        )
    def get_category(self, obj):
        return obj.product.category.name
    def get_time_hour(self, obj):
        return datetime.datetime.strftime(obj.createds, '%H:%M')
    def get_createds(self, obj):
        return datetime.datetime.strftime(obj.createds, '%d,%m,%Y')