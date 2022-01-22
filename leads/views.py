from django.shortcuts import render
from django.http import HttpResponse
from leads.models import *


# Create your views here.


def Index(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'index.html', context)
