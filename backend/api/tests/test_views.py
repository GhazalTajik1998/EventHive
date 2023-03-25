from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

import datetime
import json

from events.models import Event 
from ..serializers import UserSerializer


# Create your tests here.

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


class UserTestViews(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username = "testUser2",
            password="1234ABc"
        )
        self.client.force_authenticate(user=self.user1)
        self.user2 = get_user_model().objects.create_user(
            username = "testUser3",
            password="1234ABadsfac"
        )
        
        self.user3 = get_user_model().objects.create_user(
            username = "testUser4",
            password="1234ABfdc"
        )

        self.event1 = Event.objects.create(
            subject='Test Event 1',
            price=10,
            start_date=timezone.now(),
            end_date=timezone.now(),
            user=self.user1
        )
        self.event2 = Event.objects.create(
            subject='Test Event 2',
            price=10,
            start_date=timezone.now(),
            end_date=timezone.now(),
            user=self.user1
        )
    

    def test_user_list(self):
        # response = self.client.get(reverse('event-list'))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data[0]['subject'], 'Test Event 1')

        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], 'testUser2')

    def test_user_detail(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk':self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testUser2')

    def test_user_delete(self):
        respones = self.client.delete(reverse('user-detail', kwargs={'pk':self.user1.pk}))
        self.assertEqual(respones.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_update(self):
        response = self.client.patch(reverse('user-detail', kwargs={'pk':self.user1.pk}), data = {"first_name":"ghazal"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "ghazal")

    def test_reserve_event(self):
        response = self.client.post(reverse('reserve', kwargs={'pk':self.event1.pk})) 
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_remove_event(self):
        response = self.client.delete(reverse('remove_reserve', kwargs={'pk':self.event1.pk}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_reserved_event_of_user(self):
        self.client.post(reverse('reserve', kwargs={'pk':self.event1.pk}))
        self.client.post(reverse('reserve', kwargs={'pk':self.event2.pk})) 

        response = self.client.get(reverse('user-reserved-events', kwargs={'pk':self.user1.pk}))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['subject'], 'Test Event 1')

