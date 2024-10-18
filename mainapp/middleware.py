class RemoveOldLanguageCookieMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'django_Language' in request.COOKIES:
            response.delete_cookie('django_Language')

        return response
