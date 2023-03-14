from django.test import TestCase, SimpleTestCase

# Create your tests here.
class ListUserTest(SimpleTestCase):
    def test_list_user(self):
        response = self.client.get('')