from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta: 
        model = get_user_model()
        fields = "__all__"
