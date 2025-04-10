from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.purchase_header import PurchaseHeaderViewSet
from .views.purchase_detail import PurchaseDetailByHeaderViewSet

router = DefaultRouter()
router.register(r'purchase', PurchaseHeaderViewSet)

purchase_detail_list = PurchaseDetailByHeaderViewSet.as_view({
    'get': 'get',
    'post': 'create',
})

urlpatterns = [
    path('', include(router.urls)),
    path('purchase/<str:header_code>/details/', purchase_detail_list, name='purchase-detail-by-header'),
]
