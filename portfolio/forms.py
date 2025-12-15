from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        labels = {
            "name": "Name",
            "email": "E-Mail",
            "subject": "Betreff",
            "message": "Nachricht",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Dein Name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "dein@mail.ch", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"class": "input", "placeholder": "Worum geht es?"}),
            "message": forms.Textarea(attrs={"class": "textarea", "placeholder": "Deine Nachricht..."}),
        }
