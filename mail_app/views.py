from django.shortcuts import render
from django.views.generic import ListView


def index(request):
    return render(request, 'mail_app/newsletter_list.html')


def examples(request):
    return render(request, 'mail_app/examples_list.html')


def client(request):
    return render(request, 'mail_app/clients_list.html')
