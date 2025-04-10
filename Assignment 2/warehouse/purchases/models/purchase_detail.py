from warehouse.base_model import BaseModel
from django.db import models
from .purchase_header import PurchaseHeader

class PurchaseDetail(BaseModel):
    header_code = models.ForeignKey(PurchaseHeader, related_name='details', on_delete=models.CASCADE)
    item_code = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.header_code} - {self.item_code}"