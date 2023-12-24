from django.http import HttpResponse
from django.views.generic import View

# Create your views here.
class HelloWorldView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Hello World")
    
def check_kwargs(request, **kwargs):
    return HttpResponse(f'kwargs:<br>{kwargs}')