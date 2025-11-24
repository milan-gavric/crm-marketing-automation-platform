from rest_framework import serializers
from .models import MessageTemplate, SubjectTemplate


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubjectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

