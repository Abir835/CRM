from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from leads.models import *
from leads.forms import LeadForm, LeadModelForm, CustomUserCreationFrom, AssignAgentForm, LeadUpdateModelForm
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerLoginRequiredMixin


# CRUD+L:  Create Update Delete Retrieve + List view


# Create your views here.
class RegistrationForm(generic.CreateView):
    template_name = 'registration/registration.html'
    form_class = CustomUserCreationFrom

    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):
    template_name = 'leads/lead_home.html'


def lead_home(request):
    return render(request, 'leads/lead_home.html')


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    # list view gives context name = object_list
    # queryset = Lead.objects.all().order_by('-id')
    # customise context
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer, agent__isnull=False).order_by('-id')
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            queryset = Lead.objects.filter(agent__user=user, agent__isnull=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leeds": queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all().order_by('-id')
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = 'lead_detail'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer).order_by('-id')
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = Lead.objects.filter(agent__user=user).order_by('-id')
        return queryset


def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead_detail': lead,
    }
    return render(request, 'leads/lead_details.html', context)


class LeadCreateView(OrganizerLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('lead_list')

    def form_valid(self, form):
        send_mail(
            subject="hello abir",
            message="hello",
            from_email='abirhasan.raj.bd@gmail.com',
            recipient_list=["abirhasan.raj.bd@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = form.cleaned_data['agent']
            # lead = Lead.objects.create(
            #     first_name=first_name,
            #     last_name=last_name,
            #     age=age,
            #     agent=agent
            # )
            return redirect("/leads")
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create.html', context)


# def lead_create(request):
#     form = LeadForm()
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead = Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             return redirect("/leads")
#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_create.html', context)

class LeadUpdateView(OrganizerLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    context_object_name = 'lead'

    def get_success_url(self):
        return reverse('lead_list')

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer).order_by('-id')
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = Lead.objects.filter(agent__user=user).order_by('-id')
        return queryset


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form': form,
        'lead': lead,
    }
    return render(request, 'leads/lead_update.html', context)


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect('/leads')
#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(OrganizerLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('lead_list')

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer).order_by('-id')
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = Lead.objects.filter(agent__user=user).order_by('-id')
        return queryset


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class AssignAgentView(OrganizerLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('lead_list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()

        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update({
            'un_assign_lead': queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.is_organizer)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
        return queryset


class CategoryDetailsView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category_list'

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailsView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         'leads': leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.is_organizer)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
        return queryset


class LeadCategoryUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadUpdateModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.is_organizer)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = Lead.objects.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('lead_list')
