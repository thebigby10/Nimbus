from django import forms
from .models import File

class PublicFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('uploaded_file',)

class AuthenticatedFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'uploaded_file', 'expiry_date',)