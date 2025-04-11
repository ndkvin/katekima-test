from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['code', 'name', 'unit', 'description', 'stock', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['stock', 'balance', 'created_at', 'updated_at', 'is_deleted']

    def update(self, instance, validated_data):
        # cannot update code as it is a primary key
        # and should be unique
        validated_data.pop('code', None)
        return super().update(instance, validated_data)