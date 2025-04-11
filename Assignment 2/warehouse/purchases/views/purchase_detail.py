from rest_framework.response import Response
from ..models.purchase_detail import PurchaseDetail
from ..models.purchase_header import PurchaseHeader
from ..serializers.purchase_detail import PurchaseDetailSerializer
from rest_framework import viewsets
from items.models import Item

class PurchaseDetailByHeaderViewSet(viewsets.ViewSet):

    def get(self, request, header_code=None):
        try:
            header = PurchaseHeader.objects.get(code=header_code, is_deleted=False)
            details = PurchaseDetail.objects.filter(header_code=header, is_deleted=False)
            serializer = PurchaseDetailSerializer(details, many=True)

            response_data = {
                "code": header.code,
                "date": header.date.strftime("%Y-%m-%d") if header.date else None,
                "description": header.description,
                "details": serializer.data
            }
            return Response(response_data)
        except PurchaseHeader.DoesNotExist:
            return Response({'error': 'Header not found'}, status=404)

    def create(self, request, header_code=None):
        try:
            header = PurchaseHeader.objects.get(code=header_code, is_deleted=False)
        except PurchaseHeader.DoesNotExist:
            return Response({'error': 'Header not found'}, status=404)

        data = request.data.copy()
        data['header_code'] = header

        serializer = PurchaseDetailSerializer(data=data)
        if serializer.is_valid():
            detail = serializer.save()

            detail.remaining_quantity = data['quantity']
            detail.save()

            item_code = detail.item_code
            item = Item.objects.get(code=item_code, is_deleted=False)

            item.stock += detail.quantity
            item.balance += detail.quantity * detail.unit_price
            item.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)