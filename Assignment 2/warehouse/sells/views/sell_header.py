from ..models.sell_header import SellHeader
from rest_framework import viewsets
from ..serializers.sell_header import SellHeaderSerializer
from rest_framework.response import Response
from rest_framework import status

class SellHeaderViewSet(viewsets.ModelViewSet):
    queryset = SellHeader.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = SellHeaderSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'code'

    def get_queryset(self):
        return SellHeader.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Sell Header successfully deleted."}, status=status.HTTP_200_OK)