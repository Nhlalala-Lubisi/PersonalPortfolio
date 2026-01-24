from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Project, Certification, ProgrammingLanguage, CV
from .forms import ContactForm

def home(request):
    projects = Project.objects.all().order_by('-id')[:6]
    certs = Certification.objects.all().order_by('-date_earned')[:6]
    langs = ProgrammingLanguage.objects.all().order_by('name')
    form = ContactForm()
    cv = CV.objects.last()


    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"Portfolio contact from {name}"
            body = f"From: {name} <{email}>\n\n{message}"
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['lubisinhlaks685@gmail.com'],
            )
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")

    context = {
        'projects': projects,
        'certs': certs,
        'langs': langs,
        'form': form,
        'cv': cv,
    }
    return render(request, 'portfolio/index.html', context)
