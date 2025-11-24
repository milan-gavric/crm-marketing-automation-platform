from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('name'):
            from rest_framework import serializers as drf_serializers
            raise drf_serializers.ValidationError({'name': 'Account name is required'})
        serializer.save()

