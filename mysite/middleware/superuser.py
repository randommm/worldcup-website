from django.views.debug import technical_500_response
import sys
from django.conf import settings

class UserBasedExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if (request.user.is_superuser or
            request.META.get('REMOTE_ADDR') == '127.0.0.1'):
            return technical_500_response(request, *sys.exc_info())
