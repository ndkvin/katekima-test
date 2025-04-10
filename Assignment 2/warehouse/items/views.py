from .models import Item
from rest_framework import viewsets
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework import status

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ItemSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'code'

    def get_queryset(self):
        return Item.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Item successfully deleted."}, status=status.HTTP_200_OK)
