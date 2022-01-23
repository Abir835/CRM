from django.shortcuts import render
from django.http import HttpResponse
from leads.models import *


# Create your views here.


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context)


def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead_details': lead,
    }
    return render(request, 'leads/lead_details.html', context)
