from django.test import TestCase
from rest_framework.test import APIClient
from .models import *
import json

# Create your tests here.

def get_refresh_token():
	user          = User.objects.get(email='younes@djelloul.com')
	refresh_token = RefreshToken.objects.get(user=user).token

	return refresh_token

def get_access_token():
	user          = User.objects.get(email='younes@djelloul.com')
	access_token = AccessToken.objects.get(user=user).token

	return access_token

class TestUser(TestCase):

	def test_create_superuser_from_model(self):
		user = User.objects.create_superuser(email='younes@djelloul.com', password='younes@@456')

		self.assertEqual(user.email, 'younes@djelloul.com')
		self.assertEqual(user.first_name, None)
		self.assertEqual(user.is_staff, True)
		self.assertEqual(user.is_superuser, True)

	def test_create_normal_user_from_model(self):
		user = User.objects.create_user(email='younes@djelloul.com', password='younes@@456')

		self.assertEqual(user.email, 'younes@djelloul.com')
		self.assertEqual(user.first_name, None)

	def test_create_normal_user_from_view(self):
		client   = APIClient()
		data     = {'email': 'younesdjelloul14@gmail.com', 'password1': 'younes@@456', 'password2': 'younes@@456'}

		response = client.post('/accounts/register/', data, format='json')

		self.assertEqual(response.status_code, 201)

	def test_login_user_from_view(self):
		
		User.objects.create_user(email='younes@djelloul.com', password='younes@@456')

		client = APIClient()

		data     = {'email': 'younes@djelloul.com', 'password': 'younes@@456'}
		response = client.post('/accounts/login/', data, format='json')

		self.assertEqual(response.status_code, 200)

	def test_request_new_access_token(self):

		self.test_login_user_from_view()
		refresh_token = get_refresh_token()
		access_token  = get_access_token()

		data     = {'refresh_token': refresh_token, 'access_token': access_token}

		client   = APIClient()
		response = client.post('/accounts/access_token/refresh/', data, format='json')

		self.assertEqual(response.status_code, 201)

	def test_reset_new_password(self):

		self.test_login_user_from_view()
		access_token = get_access_token()

		data = {"access_token": access_token, "email": "younes@djelloul.com", "old_password": "younes@@456", "new_password": "younesbvb"}

		client   = APIClient()
		response = client.post('/accounts/password/reset/', data, format='json')

		self.assertEqual(response.status_code, 200)

class TestRateLimiting(TestCase):

	def test_sending_100_request_directly(self):

		TestUser().test_create_normal_user_from_model()

		data = {"email": "younes@djelloul.com", "password": "younes@@456"}

		indicator = False

		for i in range(150):
			print(i)
			client   = APIClient()
			response = client.post('/accounts/test/', data, format='json')

			if response.status_code == 429:
				indicator = True
				break

		self.assertEqual(indicator, True)