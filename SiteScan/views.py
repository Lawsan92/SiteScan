from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .Data import Data
from .forms import SiteScanForm
def index(request):
    template = loader.get_template('index.html')
    context = {}
    if request.method == 'POST':
        form = SiteScanForm(request.POST)
        if form.is_valid():
            data = Data(form.cleaned_data['user_zip'])
            dataset = data.data
            line_graph = data.graph_data_line()
            table = data.graph_data_table()
            context = {'dataset': dataset, 'line_graph': line_graph, 'table': table, 'form': form}
    else:
        form = SiteScanForm()
        context = {'form': form}
    return HttpResponse(template.render(context, request))