from warehouse.base_model import BaseModel
from django.db import models

class Item(BaseModel):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    # Stock dan Balance hanya bisa berubah lewat proses pembelian/penjualan
    stock = models.PositiveIntegerField(default=0, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    def __str__(self):
        return self.code