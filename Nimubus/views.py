from django.shortcuts import render

# Create your views here.
def home(request):
    # if the user is logged in show one view
    context = {
        "title":"homepage"
    }
    # if the user is not logged in show public view
    return render(request ,'Nimbus/index.html', context)

