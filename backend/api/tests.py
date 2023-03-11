from django.test import TestCase
from rest_framework.tests import APITestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class UserListAPIViewTestCase(APITestCase):
    url = reverse('user-list')

    def test_get_user_list(self):
        user1 = get_user_model().objects.create(username='user1')
        user2 = get_user_model().objects.create(username='user2')
        serializer = UserSerializer([user1, user2], many=True)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
