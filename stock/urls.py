from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryMVS, BrandMVS, FirmMVS, ProductMVS, PurchasesMVS, SalesMVS
router = DefaultRouter()

router.register('categories', CategoryMVS)
router.register('brands', BrandMVS)
router.register('firms', FirmMVS)
router.register('products', ProductMVS)
router.register('purchases', PurchasesMVS)
router.register('sales', SalesMVS)

urlpatterns = [
path('', include(router.urls)),    
]
