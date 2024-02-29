from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden


class AllowAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = settings.ACCESS_ALLOWED_START_TIME
        end_time = settings.ACCESS_ALLOWED_END_TIME

        if datetime.strptime(start_time, '%H:%M').time() <= current_time <= datetime.strptime(end_time, '%H:%M').time():
            return self.get_response(request)
        else:
            return HttpResponseForbidden(f"Access is allowed between {start_time} and {end_time}")
