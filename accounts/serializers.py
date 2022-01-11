from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

	id        = serializers.IntegerField(read_only=True)
	password1 = serializers.CharField(write_only=True)
	password2 = serializers.CharField(write_only=True)

	class Meta:
		model  = User
		fields = ['id', 'email', 'password1', 'password2']

	def validate(self, attrs):
		
		email     = attrs.get('email')
		password1 = attrs.get('password1')
		password2 = attrs.get('password2')

		if not email or not password1 or not password2:
			raise serializers.ValidationError('email is required.')
		if password1 != password2:
			raise serializers.ValidationError('passwords didn\'t match')

		attrs['password'] = attrs['password1']
		del attrs['password1']
		del attrs['password2']

		return attrs

	def create(self, validated_data):
		return User.objects.create(**validated_data)