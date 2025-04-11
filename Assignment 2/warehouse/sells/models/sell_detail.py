from warehouse.base_model import BaseModel
from django.db import models
from .sell_header import SellHeader

class SellDetail(BaseModel):
    header_code = models.ForeignKey(SellHeader, related_name='details', on_delete=models.CASCADE)
    item_code = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.header_code} - {self.item_code}"