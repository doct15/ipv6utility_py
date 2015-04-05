#from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from ipv6app.forms import formOptions
from django.template import RequestContext
#from django.views.generic.edit import FormView


def index(request):
    #return HttpResponse("Brian says hello world!")
    context = RequestContext(request)
    if request.method == 'POST':
        inipv6address = request.POST['inipv6address']
        myForm = formOptions(request.POST)
    #   if myForm.is_valid():
    #        #return HttpResponseRedirect('/thanks/')
    #        return render_to_response('ipv6app/index.html', {
    #            'form': myForm,
    #        })
    else:
        myForm = formOptions()
    #
    #return render_to_response('ipv6app/index.html', {
    #    'form': myForm,
    #})
    
    # if myform.is_valid():
    # data = myform.cleaned_data
    # field = data['field']
    
    #context_dict = {'boldmessage': "I am bold font from the context"}
    #context = {}
    return render_to_response('ipv6app/index.html', {'form': myForm}, context)
    #return render('ipv6app/index.html', {'form': myForm})
    
def about(request):
    return HttpResponse("Brian says hello world!")

