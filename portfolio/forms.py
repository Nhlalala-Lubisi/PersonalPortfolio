from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'placeholder': 'Your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5, 'placeholder': 'Your message'
    }))
