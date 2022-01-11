from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from .operations import *
from datetime import datetime
from django.utils import timezone

# Create your views here.

class UserRegistrationView(APIView):

	serializer_class = UserSerializer

	def post(self, request):
		data = request.data

		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class UserLoginView(APIView):

	def post(self, request):

		email    = request.data.get('email')
		password = request.data.get('password')

		if not User.objects.filter(email=email).exists():
			return Response('User not found.', status=400)

		if not email or not password:
			return Response('Invalid information', status=400)

		user = authenticate(email=email, password=password)

		if not user:
			return Response('Invalid information', status=400)

		refresh_token = create_refresh_token(user=user)[0]
		access_token  = create_access_token(user=user)[0]

		# saving token in the db
		RefreshToken.objects.create(user=user, token=refresh_token, expire=create_refresh_token(user=user)[1])
		AccessToken.objects.create(user=user, token=access_token, expire=create_access_token(user=user)[1])

		return Response({'refresh_token': refresh_token, 'access_token': access_token}, status=200)

class RefreshAccessTokenView(APIView):

	authenticated = True

	def post(self, request):
		
		refresh_token = request.data.get('refresh_token')

		if not RefreshToken.objects.filter(token=refresh_token).exists():
			return Response('Refresh Token Not Found', status=404)

		obj = RefreshToken.objects.get(token=refresh_token)

		if obj.user != request.user:
			return Response('Access Denied', status=400)

		if obj.expire < timezone.now():
			AccessToken.objects.get(user=request.user).delete()
			obj.delete()

			return Response('Refresh Token Expired', status=400)

		user = request.user

		access_token     = AccessToken.objects.get(user=user).delete()
		new_access_token = create_access_token(user=user)

		return Response({'access_token': new_access_token}, status=201)

class ResetPasswordView(APIView):

	authenticated = True

	def post(self, request):

		email        = request.data.get('email')
		old_password = request.data.get('old_password')
		new_password = request.data.get('new_password')

		user = authenticate(email=email, password=old_password)

		if not user:
			return Response('Old Password didn\'t match', status=400)

		user.set_password(new_password)
		user.save()

		return Response('Password Changed Successfully', status=200)