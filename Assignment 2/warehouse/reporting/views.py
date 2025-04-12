from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from items.models import Item
from purchases.models.purchase_detail import PurchaseDetail
from sells.models.sell_detail import SellDetail
from datetime import datetime

def split_transaction_by_fifo(entry, stock_used):
    stock_prices = entry["stock_price"]
    split_entries = []

    for used_qty, price in zip(stock_used, stock_prices):
        if used_qty == 0:
            continue
        split_entry = entry.copy()
        split_entry["out_qty"] = used_qty
        split_entry["out_price"] = price
        split_entry["out_total"] = used_qty * price
        split_entries.append(split_entry)

    return split_entries

class ReportView(APIView):
    def get(self, request, item_code):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        try:
            item = Item.objects.get(code=item_code, is_deleted=False)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception:
            return Response({'error': 'Invalid date format. Use yyyy-mm-dd'}, status=400)

        purchases = PurchaseDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start, end),
            is_deleted=False
        ).select_related('header_code')

        sales = SellDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start, end),
            is_deleted=False
        ).select_related('header_code')

        transactions = []

        for p in purchases:
            transactions.append({
                "type": "purchase",
                "date": p.header_code.date,
                "description": p.header_code.description,
                "code": p.header_code.code,
                "quantity": p.quantity,
                "price": p.unit_price,
            })

        for s in sales:
            transactions.append({
                "type": "sale",
                "date": s.header_code.date,
                "description": s.header_code.description,
                "code": s.header_code.code,
                "quantity": s.quantity,
            })

        transactions.sort(key=lambda x: x['date'])

        report = []
        stock_qty = []
        stock_price = []
        stock_total = []
        balance_qty = 0
        balance = 0

        for trx in transactions:
            if trx["type"] == "purchase":
                in_qty = trx["quantity"]
                in_price = trx["price"]
                in_total = in_qty * in_price

                stock_qty.append(in_qty)
                stock_price.append(in_price)
                stock_total.append(in_total)

                balance_qty += in_qty
                balance += in_total

                report.append({
                    "date": trx["date"].strftime("%d-%m-%Y"),
                    "description": trx["description"],
                    "code": trx["code"],
                    "in_qty": in_qty,
                    "in_price": in_price,
                    "in_total": in_total,
                    "out_qty": 0,
                    "out_price": 0,
                    "out_total": 0,
                    "stock_qty": stock_qty.copy(),
                    "stock_price": stock_price.copy(),
                    "stock_total": stock_total.copy(),
                    "balance_qty": balance_qty,
                    "balance": balance,
                })
            else:
                remaining = trx["quantity"]
                i = 0

                while remaining > 0 and i < len(stock_qty):
                    if stock_qty[i] == 0:
                        i += 1
                        continue

                    used = min(remaining, stock_qty[i])
                    price = stock_price[i]
                    total = used * price

                    stock_qty[i] -= used
                    stock_total[i] = stock_qty[i] * stock_price[i]

                    # Jika stok habis, set price dan total ke 0
                    if stock_qty[i] == 0:
                        stock_price[i] = 0
                        stock_total[i] = 0

                    balance_qty -= used
                    balance -= total

                    report.append({
                        "date": trx["date"].strftime("%d-%m-%Y"),
                        "description": trx["description"],
                        "code": trx["code"],
                        "in_qty": 0,
                        "in_price": 0,
                        "in_total": 0,
                        "out_qty": used,
                        "out_price": price,
                        "out_total": total,
                        "stock_qty": stock_qty.copy(),
                        "stock_price": stock_price.copy(),
                        "stock_total": stock_total.copy(),
                        "balance_qty": balance_qty,
                        "balance": balance,
                    })

                    remaining -= used
                    i += 1

        result = {
            "result": {
                "items": report,
                "item_code": item.code,
                "name": item.name,
                "unit": item.unit,
                "summary": {
                    "in_qty": sum(trx['in_qty'] for trx in report),
                    "out_qty": sum(trx['out_qty'] for trx in report),
                    "balance_qty": balance_qty,
                    "balance": balance
                }
            }
        }

        return Response(result)