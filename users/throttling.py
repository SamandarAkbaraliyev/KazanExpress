from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from datetime import datetime, timedelta


class LoginThrottle(BaseThrottle):
    THROTTLE_MINUTES = [15, 20, 40, 60]

    def allow_request(self, request, view):
        username = request.data.get('username')
        if username:
            cache_key = f'login_throttle_{username}'
            attempt_count = cache.get(cache_key, 0)

            throttle_index = min(attempt_count, len(self.THROTTLE_MINUTES) - 1)
            throttle_duration = self.THROTTLE_MINUTES[throttle_index]

            last_attempt_time = cache.get(f'last_login_attempt_{username}')
            if last_attempt_time and datetime.now() - last_attempt_time < timedelta(minutes=throttle_duration):
                return False
            else:
                cache.set(cache_key, attempt_count + 1, throttle_duration * 60)
                cache.set(f'last_login_attempt_{username}', datetime.now())
                return True
        return True
