from rest_framework import serializers
from ..models.purchase_header import PurchaseHeader

class PurchaseHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description']
        read_only_fields = ['created_at', 'updated_at', 'is_deleted']
