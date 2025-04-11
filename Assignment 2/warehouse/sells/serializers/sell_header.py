from rest_framework import serializers
from ..models.sell_header import SellHeader

class SellHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description']
        read_only_fields = ['created_at', 'updated_at', 'is_deleted']
