import json
from functools import wraps
from django.core.cache import caches
from django.http import JsonResponse as Response

redis_client = caches['default'].client

class Cache(object):
    @classmethod
    def get(cls, key):
        value = redis_client.get(key)
        if isinstance(value, bytes):
            value = value.decode()
        return value

    @classmethod
    def set(cls, key, value, ttl=0):
        redis_client.set(*[key, value, ttl])

    @classmethod
    def cache_api_response(
        cls,
        key= None,
        timeout=60*60,
        status_code=200,
    ):
    
        """Decorator can cache the response of an api.

        Usage:
            @action(detail=False, methods=["get"], url_path="dummy-api")
            @cache_reponse(timeout=60 * 60)
            def view(request):
            
            You can also configure response class to support both Django and DRF Views.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal key
                nonlocal timeout

                if not key:
                    key = func.__name__
                cache_data = cls.get(key)
                if cache_data:
                    data = json.loads(cache_data)
                    return Response(data, status=status_code)
                else:
                    response = func(*args, **kwargs)
                    data = response.content.decode("utf-8")
                    cls.set(key, data, timeout)
                    return response

            return wrapper

        return decorator