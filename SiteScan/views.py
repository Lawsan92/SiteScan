from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .Data import Data
from .forms import SiteScanForm


data = Data('78730')
dataset = data.data
line_graph = data.graph_data_line()
table = data.graph_data_table()
def index(request):
    template = loader.get_template('index.html')
    if request.method == 'POST':
        form = SiteScanForm(request.POST)
        if form.is_valid():
            print('form.data:', form.cleaned_data)
            Data(form.cleaned_data['user_zip']).print()
            print(Data(form.cleaned_data['user_zip']))
    else:
        form = SiteScanForm()
    context = {'dataset': dataset, 'line_graph': line_graph, 'table': table, 'form': form}
    return HttpResponse(template.render(context, request))

def test(request):
    return HttpResponse("Hello, test!")