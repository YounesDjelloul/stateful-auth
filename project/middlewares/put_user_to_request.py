from accounts.models import *
from django.http import HttpResponseForbidden
import ast
from accounts.operations import check_token_not_expired

class PutUser(object):
	
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):

		if view_func.view_class.__name__ == "RefreshAccessTokenView":

			bytes_request_data = getattr(request, '_body', request.body)
			data               = ast.literal_eval(bytes_request_data.decode('utf-8'))

			access_token       = data.get('access_token')

			if AccessToken.objects.filter(token=access_token).exists():

				user         = AccessToken.objects.get(token=access_token).user
				request.user = user

				return None
			else:
				return HttpResponseForbidden('Access Denied')	
		
		try:
			auth = view_func.view_class.authenticated

			bytes_request_data = getattr(request, '_body', request.body)
			data               = ast.literal_eval(bytes_request_data.decode('utf-8'))

			if auth:
				access_token = data.get('access_token')

				if AccessToken.objects.filter(token=access_token).exists():

					check = check_token_not_expired(AccessToken.objects.get(token=access_token))

					if check:
						user = AccessToken.objects.get(token=access_token).user
						request.user = user
					else:
						return HttpResponseForbidden('Access Token Expired')
				else:
					return HttpResponseForbidden('Access Denied')
			else:
				return None
		except:
			return None