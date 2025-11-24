from rest_framework import serializers
from .models import Email
from accounts.serializers import AccountSerializer


class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer for Email model
    """
    account_details = AccountSerializer(source='account', read_only=True)

    class Meta:
        model = Email
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        return value.lower().strip()
