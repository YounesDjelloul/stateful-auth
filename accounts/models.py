from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email, password):
		user = User.objects.create(email=email)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password):
		if not password:
			return 'Password is required'
		
		user = User.objects.create(email=email, is_staff=True, is_superuser=True)
		user.set_password(password)
		user.save()
		return user

class User(AbstractUser):

	first_name = None
	last_name  = None
	username  = None
	email     = models.EmailField(unique=True)

	USERNAME_FIELD  = 'email'
	REQUIRED_FIELDS = []
	objects         = UserManager()

	def __str__(self):
		return str(self.email)


class RefreshToken(models.Model):

	user   = models.OneToOneField(User, on_delete=models.CASCADE)
	token  = models.CharField(max_length=500, editable=False)
	expire = models.DateTimeField()

	def __str__(self):
		return str(self.user)


class AccessToken(models.Model):

	user   = models.OneToOneField(User, on_delete=models.CASCADE)
	token  = models.CharField(max_length=500, editable=False)
	expire = models.DateTimeField()

	def __str__(self):
		return str(self.user)


class ListIp(models.Model):

	ip     = models.CharField(max_length=20)
	number = models.PositiveIntegerField()
	expire = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.ip + " - " + str(self.number)

class BlackList(models.Model):

	ip     = models.CharField(max_length=20)
	expire = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.ip)