from django.http import JsonResponse
from django.utils import timezone
from accounts.models import *

class RateLimiting:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		return response

	def process_view(self, request, view_func, view_args, view_kwargs):

		ip  = request.META.get("REMOTE_ADDR")
		now = timezone.now()

		if BlackList.objects.filter(ip=ip).exists():

			obj = BlackList.objects.get(ip=ip)

			if now < obj.expire:
				return JsonResponse({"response": "You are blocked"}, status=400)

			obj.delete()

		if ListIp.objects.filter(ip=ip).exists():

			obj = ListIp.objects.get(ip=ip)

			if now < obj.expire:
				obj.number += 1
				obj.save()

				if obj.number > 100:
					BlackList.objects.create(ip=ip)

		return JsonResponse({"response": "Too Many Requests"}, status=429)