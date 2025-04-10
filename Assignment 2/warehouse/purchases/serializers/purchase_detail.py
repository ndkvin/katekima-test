from rest_framework import serializers
from ..models.purchase_detail import PurchaseDetail
from ..models.purchase_header import PurchaseHeader

class PurchaseDetailSerializer(serializers.ModelSerializer):
    header_code = serializers.SlugRelatedField(
        queryset=PurchaseHeader.objects.all(),
        slug_field='code',
        required=False,
        allow_null=True
    )

    class Meta:
        model = PurchaseDetail
        fields = ['item_code', 'quantity', 'unit_price', 'header_code']
        read_only_fields = ['created_at', 'updated_at', 'is_deleted']