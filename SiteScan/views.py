from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def test(request):
    return HttpResponse("Hello, test!")