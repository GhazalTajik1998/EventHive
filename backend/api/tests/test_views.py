from django.test import TestCase, SimpleTestCase, Client
from rest_framework.test import APITestCase
import datetime
import json
# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from ..serializers import UserSerializer
from events.models import Event 
from django.utils import timezone


class EventTestViews(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
        self.event1 = Event.objects.create(
            subject='Test Event 1',
            price=10,
            start_date=timezone.now(),
            end_date=timezone.now(),
            user=self.user
        )
        self.event2 = Event.objects.create(
            subject='Test Event 2',
            price=10,
            start_date=timezone.now(),
            end_date=timezone.now(),
            user=self.user
        )

    def test_event_list(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['subject'], 'Test Event 1')

    def test_user_detail(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_event_delete(self):
        response = self.client.delete(reverse('event-detail', kwargs={'pk': self.event2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_event_update(self):
        data = {
        'price': 30,
        'start_date': str(self.event1.start_date),
        'end_date': str(datetime.datetime(2024, 3, 14, 12, 0, 0)),
        }
        response = self.client.patch(reverse('event-detail', kwargs={'pk': self.event1.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content.decode('utf-8'))
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.price, 30)


