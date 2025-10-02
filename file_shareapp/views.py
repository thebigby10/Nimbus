from django.shortcuts import render, redirect
from .forms import PublicFileForm
from .models import File

from django.utils import timezone
from datetime import timedelta

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

def public_view(request):
    if request.method == 'POST':
        print("Received a POST request.")
        form = PublicFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid. Attempting to save...")
            print(f">>> [VIEW CHECK] DEFAULT_FILE_STORAGE is: {settings.DEFAULT_FILE_STORAGE}")
            try:
                new_file = form.save(commit=False)

                uploaded_file = request.FILES['uploaded_file']
                new_file.title = uploaded_file.name
                new_file.expiry_date = timezone.now().date() + timedelta(days=7)
                new_file.save()
                print("Form save successful!")
                return redirect('file_shareapp:success_page')
            except Exception as e:
                print("--- AN ERROR OCCURRED DURING SAVE ---") 
                print(e)
                logger.exception("File upload to MinIO failed.")

    else:
        print("--- FORM IS NOT VALID ---")
        form = PublicFileForm()
        
    return render(request ,'file_shareapp/public/index.html', {'form':form})


def auth_view(request):
    return render(request ,'file_shareapp/authenticated/index.html')


def file_list(request):
    documents = File.objects.all()
    return render(request, 'file_shareapp/file_list.html', {'documents': documents})

def success_view(request):
    return render(request, 'file_shareapp/success.html');

def file_detail(request):
    