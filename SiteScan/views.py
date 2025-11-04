from django.http import HttpResponse
from django.template import loader
from SiteScan import API_fetch, draw_line_graph
dataset = API_fetch('78735')
graph = draw_line_graph(dataset)
def index(request):
    template = loader.get_template('index.html')
    context = {'dataset': dataset}
    return HttpResponse(template.render(context, request))

def test(request):
    return HttpResponse("Hello, test!")