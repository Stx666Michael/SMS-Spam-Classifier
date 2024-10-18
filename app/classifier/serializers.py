# classifier/serializers.py
from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
    sms = serializers.CharField()
