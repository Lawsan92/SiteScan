from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .DataUI import Data
from .forms import SiteScanForm
def index(request):
    template = loader.get_template('index.html')
    context = {}
    if request.method == 'POST':
        form = SiteScanForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['user_zip']
            data = Data(zip_code)
            data.API_fetch()
            data.model_data()
            dataset = data.data
            err = ''
            if not data:
                table = []
                line_graph = []
                err = 'No data found for this zip code'
            else:
                line_graph = data.graph_data_line()
                table = data.graph_data_table()
            context = {'dataset': dataset, 'line_graph': line_graph, 'table': table, 'form': form, 'err' : err}
    else:
        form = SiteScanForm()
        context = {'form': form}
    return HttpResponse(template.render(context, request))