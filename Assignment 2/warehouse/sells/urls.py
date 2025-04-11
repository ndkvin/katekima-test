from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.sell_header import SellHeaderViewSet
from .views.sell_detail import SellDetailByHeaderViewSet

router = DefaultRouter()
router.register(r'sell', SellHeaderViewSet)

purchase_detail_list = SellDetailByHeaderViewSet.as_view({
    'get': 'get',
    'post': 'create',
})

urlpatterns = [
    path('', include(router.urls)),
    path('sell/<str:header_code>/details/', purchase_detail_list, name='sell-detail-by-header'),
]
