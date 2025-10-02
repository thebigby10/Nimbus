from django.shortcuts import render, redirect
from .forms import PublicFileForm
from .models import File

from django.utils import timezone
from datetime import timedelta

import logging

from django.conf import settings

from django.shortcuts import get_object_or_404

import os

from django.http import FileResponse, Http404

logger = logging.getLogger(__name__)

def public_view(request):
    if request.method == 'POST':
        print("Received a POST request.")
        form = PublicFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                new_file = form.save(commit=False)

                uploaded_file = request.FILES['uploaded_file']
                new_file.title = uploaded_file.name
                new_file.expiry_date = timezone.now().date() + timedelta(days=7)
                new_file.save()
                return redirect('file_shareapp:file_detail_view', file_id = new_file.id)
            except Exception as e:
                print(e)
                logger.exception("File upload to MinIO failed.")

    else:
        form = PublicFileForm()
        
    return render(request ,'file_shareapp/public/index.html', {'form':form})


def auth_view(request):
    return render(request ,'file_shareapp/authenticated/index.html')


# def file_list(request):
#     documents = File.objects.all()
#     return render(request, 'file_shareapp/file_list.html', {'documents': documents})

# def success_view(request):
#     return render(request, 'file_shareapp/success.html');

def file_detail(request, file_id):
    file_data = get_object_or_404(File, id=file_id)
    context = {
        'file_upload': file_data,
        'BASE_URL': 'http://localhost:8000'
    }
    return render(request, 'file_shareapp/file_detail.html', context)

def file_download(request,file_id):
    uploaded_file = get_object_or_404(File, pk=file_id)

    file_path = uploaded_file.uploaded_file.path

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        return response

    raise Http404