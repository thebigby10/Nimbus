from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "name":"homepage"
    }
    return render(request ,'Nimbus/index.html', context)