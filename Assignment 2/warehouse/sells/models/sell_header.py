from warehouse.base_model import BaseModel
from django.db import models

class SellHeader(BaseModel):
    code = models.CharField(max_length=50, primary_key=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code
    
