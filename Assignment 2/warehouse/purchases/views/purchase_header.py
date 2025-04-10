from ..models.purchase_header import PurchaseHeader
from rest_framework import viewsets
from ..serializers.purchase_header import PurchaseHeaderSerializer
from rest_framework.response import Response
from rest_framework import status

class PurchaseHeaderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHeader.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = PurchaseHeaderSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'code'

    def get_queryset(self):
        return PurchaseHeader.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Purchase Header successfully deleted."}, status=status.HTTP_200_OK)