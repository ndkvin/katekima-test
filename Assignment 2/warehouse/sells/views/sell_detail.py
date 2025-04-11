from rest_framework.response import Response
from ..models.sell_detail import SellDetail
from ..models.sell_header import SellHeader
from ..serializers.sell_detail import SellDetailSerializer
from rest_framework import viewsets
from items.models import Item
from purchases.models.purchase_detail import PurchaseDetail

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

        item_code = data['item_code']
        item = Item.objects.get(code=item_code, is_deleted=False)
        quantity_to_sell = int(data['quantity'])

        if item.stock < quantity_to_sell:
            return Response({'error': 'Insufficient stock'}, status=400)

        # Ambil list pembelian (FIFO)
        purchases = PurchaseDetail.objects.filter(
            item_code=item_code,
            remaining_quantity__gt=0,
            is_deleted=False,
            header_code__date__lte=header.date
        ).order_by('header_code__date')

        quantity_left = quantity_to_sell
        total_cost = 0

        for purchase in purchases:
            if quantity_left == 0:
                break

            take_qty = min(quantity_left, purchase.remaining_quantity)
            total_cost += take_qty * purchase.unit_price

            purchase.remaining_quantity -= take_qty
            purchase.save()

            quantity_left -= take_qty

        serializer = SellDetailSerializer(data=data)

        if serializer.is_valid():
            detail = serializer.save()

            item.stock -= detail.quantity
            item.balance -= total_cost
            item.save()

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)