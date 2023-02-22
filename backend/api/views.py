from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from account.models import User
from .serializers import UserSerializer, EventSerializer
from events.models import Event

# Create your views here.
class UserListView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class =  UserSerializer
    permission_classes = [IsAuthenticated]


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer




