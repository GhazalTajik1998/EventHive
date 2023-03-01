from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from events.models import Event


class UserSerializer(ModelSerializer):
    # Attach method to field for displaying
    full_name = serializers.CharField(source='get_full_name')
    class Meta: 
        model = get_user_model()
        fields = "__all__"


class EventSerializer(ModelSerializer):
    
    # Change the fields name for displaying
    # start = serializers.DateTimeField(source='start_date')

    # Check this out
    user = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = "__all__"

    # Object-level Validation
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('End date must be after start date')
        return data

    # Custom level validation
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price can not be smaller than zero")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Custom'] = "What's up"
        return representation

    def get_user(self, obj):
            return {
                "username" : obj.user.username,
                "first_name" : obj.user.first_name,
            }