from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from events.models import Event


class UserSerializer(ModelSerializer):
    class Meta: 
        model = get_user_model()
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
