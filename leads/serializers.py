from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    Email = serializers.EmailField(required=False)
    email = serializers.EmailField(source='Email', required=False)

    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Handle both 'Email' and 'email' field names
        if 'email' in data:
            data['Email'] = data.pop('email')
        if 'Email' in data:
            data['Email'] = data['Email'].lower().strip()
        if not data.get('Email'):
            raise serializers.ValidationError({'Email': 'Email is required'})
        return data

