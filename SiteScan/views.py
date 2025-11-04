from django.http import HttpResponse
from django.template import loader
from SiteScan import Data

data = Data('78735')
dataset = data.data
line_graph = data.graph_data_line()
table = data.graph_data_table()

def index(request):
    template = loader.get_template('index.html')
    context = {'dataset': dataset, 'line_graph': line_graph, 'table': table}
    return HttpResponse(template.render(context, request))

def test(request):
    return HttpResponse("Hello, test!")