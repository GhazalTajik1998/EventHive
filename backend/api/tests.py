from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class UserListAPIViewTestCase(TestCase):

    def test_create_model(self):
        model = get_user_model().objects.create(username="test")


        self.assertEqual(model.username, 'test')



