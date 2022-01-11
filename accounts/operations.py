from .models import *
import jwt
from datetime import datetime, timedelta
from django.utils import timezone

def create_refresh_token(user):

	expire  = datetime.now() + timedelta(days=365)

	payload = {'id': user.id, 'time': str(expire)}
	token   = jwt.encode(payload, 'refresh', algorithm="HS256")

	return [token, expire]

def create_access_token(user):

	expire  = datetime.now() + timedelta(days=1)

	payload = {'id': user.id, 'time': str(expire)}
	token   = jwt.encode(payload, 'access', algorithm="HS256")

	return [token, expire]

def check_token_not_expired(AccessToken):

	if timezone.now() > AccessToken.expire:
		return False

	return True