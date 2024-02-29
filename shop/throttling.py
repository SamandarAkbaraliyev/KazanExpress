import datetime
from rest_framework.throttling import BaseThrottle


class DynamicTimeRestrictedThrottle(BaseThrottle):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def allow_request(self, request, view):
        now = datetime.datetime.now().time()
        if self.start_time <= now <= self.end_time:
            return True
        return False
