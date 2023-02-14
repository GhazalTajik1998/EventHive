from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from account.models import User
from .serializers import UserSerializer
# Create your views here.


class UserListView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class =  UserSerializer



