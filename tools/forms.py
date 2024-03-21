from django import forms
from .models import txttoaduiodata
class TTSForm(forms.ModelForm):
    class Meta:
        model = txttoaduiodata
        fields = ['text','voicer','speed','pitch','volume','audio_format']

