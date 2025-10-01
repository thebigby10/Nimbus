from django.shortcuts import render


def public_view(request):
    return render(request ,'file_shareapp/public/index.html')

def auth_view(request):
    return render(request ,'file_shareapp/authenticated/index.html')