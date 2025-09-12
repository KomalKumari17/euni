# throttles.py
from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled
import redis
from django.utils.timezone import now

r = redis.Redis(host='localhost', port=6379, db=0)

class UserRateThrottle(BaseThrottle):
    RATE_LIMIT = 20
    DURATION = 60

    def allow_request(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return True 

        key = f"user_throttle:{request.user.id}:{now().strftime('%Y%m%d%H%M')}"
        count = r.incr(key)
        if count == 1:
            r.expire(key, self.DURATION)

        ttl = r.ttl(key)
        if ttl is None or ttl < 0:
            ttl = self.DURATION

        if count > self.RATE_LIMIT:
            raise Throttled(detail=f"Too many requests. Try again in {ttl} seconds.", wait=ttl)
        return True

class IPRateThrottle(BaseThrottle):
    RATE_LIMIT = 50   
    DURATION = 60 

    def get_ident(self, request):
        """Returns IP address of the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_cache_key(self, ip):
        current_minute = now().strftime('%Y%m%d%H%M')
        return f"ip_throttle:{ip}:{current_minute}"

    def allow_request(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        ip = self.get_ident(request)
        key = self.get_cache_key(ip)

        current_count = r.incr(key)
        if current_count == 1:
            r.expire(key, self.DURATION)

        ttl = r.ttl(key)

        if current_count > self.RATE_LIMIT:
            raise Throttled(
                detail=f"Too many requests. Try again in {ttl} seconds.",
                wait=ttl
            )

        return True
