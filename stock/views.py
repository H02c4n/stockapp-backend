from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Firm, Brand, Sales, Product, Purchases
from .serializers import CategorySerializer, CategoryProductSerializer , BrandSerializer, FirmSerializer, ProductSerializer, PurchasesSerializer, SalesSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions

from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class CategoryMVS(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']  #? http://127.0.0.1:8000/stock/categories/?search=t
    filterset_fields=['name'] #! http://127.0.0.1:8000/stock/categories/?name=Clothing
    permission_classes =[DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.query_params.get('name'):
            return CategoryProductSerializer
        return super().get_serializer_class()



class BrandMVS(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends =[filters.SearchFilter]
    search_fields=['name']




class FirmMVS(ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class ProductMVS(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields =['category', 'brand']



class PurchasesMVS(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['firm']
    filterset_fields =['firm', 'product']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #! ################ADD PRD STOCK####################
        purchase = request.data
        product = Product.objects.get(id=purchase['product_id'])
        product.stock += purchase['quantity']
        product.save()


        #! #################################################
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #! #####################UPDATE PRD STOCK##############
        purchase = request.data
        product = Product.objects.get(id=purchase['product_id'])

        result = purchase['quantity'] - instance.quantity

        product.stock += result
        product.save()




        #! ###################################################
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        product = Product.objects.get(id=instance.product_id)
        product.stock -= instance.quantity
        product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class SalesMVS(ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['brand']
    filterset_fields =['brand', 'product']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #! ################REDUCE PRD STOCK####################
        sales = request.data
        product = Product.objects.get(id=sales['product_id'])

        if sales['quantity'] <= product.stock:
            product.stock -= sales['quantity']
            product.save()
        else:
            data = {
                "message" : f"We dont have enough stock!! Only *{product.stock}* left"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        


        #! #################################################
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #! #####################UPDATE PRD STOCK##############
        sales = request.data
        product = Product.objects.get(id=instance.product_id)

        if sales['quantity'] > instance.quantity:

            if sales['quantity'] <= instance.quantity + product.stock:
                product.stock = instance.quantity + product.stock -sales['quantity']
                product.save()
            else:
                data={
                    'message':"Olmaz"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif instance.quantity >= sales['quantity']:
            product.stock += instance.quantity -sales['quantity']
            product.save()


        # result = sales['quantity'] - instance.quantity

        # product.stock += result
        # product.save()




        #! ###################################################
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        #!####### DELETE Product Stock ########
        product = Product.objects.get(id=instance.product_id)
        product.stock += instance.quantity
        product.save()
        #!##################################
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)