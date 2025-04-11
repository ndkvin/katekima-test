from rest_framework.response import Response
from ..models.sell_detail import SellDetail
from ..models.sell_header import SellHeader
from ..serializers.sell_detail import SellDetailSerializer
from rest_framework import viewsets
from items.models import Item

class SellDetailByHeaderViewSet(viewsets.ViewSet):

    def get(self, request, header_code=None):
        try:
            print(header_code)
            header = SellHeader.objects.get(code=header_code, is_deleted=False)
            details = SellDetail.objects.filter(header_code=header, is_deleted=False)
            serializer = SellDetailSerializer(details, many=True)

            response_data = {
                "code": header.code,
                "date": header.date.strftime("%Y-%m-%d") if header.date else None,
                "description": header.description,
                "details": serializer.data
            }
            return Response(response_data)
        except SellHeader.DoesNotExist:
            return Response({'error': 'Header not found'}, status=404)

    def create(self, request, header_code=None):
        try:
            header = SellHeader.objects.get(code=header_code, is_deleted=False)
        except SellHeader.DoesNotExist:
            return Response({'error': 'Header not found'}, status=404)

        data = request.data.copy()
        data['header_code'] = header
        serializer = SellDetailSerializer(data=data)
        if serializer.is_valid():
            detail = serializer.save()

            item_code = detail.item_code
            item = Item.objects.get(code=item_code, is_deleted=False)

            if item.stock < detail.quantity:
                return Response({'error': 'Insufficient stock'}, status=400)
            
            # decrease the stock based on the quantity sold
            item.stock -= detail.quantity
            # decrease the balance based on the average cost
            item.balance -= detail.quantity * (item.balance/item.stock)
            item.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)