from django.shortcuts import render
from django.shortcuts import reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from agents.forms import AgentModelFrom
from agents.mixins import OrganizerLoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
# Create your views here.


class AgentListView(OrganizerLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganizerLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelFrom

    def get_success_url(self):
        return reverse('agents:agent_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.password(random.randint(0, 100000))
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        # agent = form.save(commit=False)
        # agent.organization = self.request.user.userprofile
        # agent.save()
        send_mail(subject="hello agent", message="invite agent",
                  from_email='demo@gmail.com',
                  recipient_list=[user.email])

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_details.html'
    queryset = Agent.objects.all()
    context_object_name = 'agent_detail'


class AgentUpdateView(OrganizerLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelFrom
    queryset = Agent.objects.all()
    context_object_name = 'update_agent'

    def get_success_url(self):
        return reverse('agents:agent_detail')


class AgentDeleteView(OrganizerLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'delete_agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agents:agent_list')
