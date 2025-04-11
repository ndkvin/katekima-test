from rest_framework import serializers
from ..models.sell_detail import SellDetail
from ..models.sell_header import SellHeader

class SellDetailSerializer(serializers.ModelSerializer):
    header_code = serializers.SlugRelatedField(
        queryset=SellHeader.objects.all(),
        slug_field='code',
        required=False,
        allow_null=True
    )

    class Meta:
        model = SellDetail
        fields = ['item_code', 'quantity', 'header_code']
        read_only_fields = ['created_at', 'updated_at', 'is_deleted', 'header_code']