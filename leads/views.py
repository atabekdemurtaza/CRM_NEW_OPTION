from django.shortcuts import render
from .models import Leads
from .models import Agent
from django.shortcuts import redirect
from .forms import LeadModelCreateForm
from django.views.generic import TemplateView
from django.views import generic
from leads.forms import CustomUserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

#from django.contrib.auth.views import PasswordChangeDoneView
#CRUD -> Create, Retrieve, Update, Delete

class SignUpView(generic.CreateView):

    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    #success_url = reverse_lazy('leads:lead_list')

    def get_success_url(self):
        return reverse('login')

#New Version
class LeadListView(LoginRequiredMixin, generic.ListView):

    template_name = 'leads/lead-list.html'
    queryset = Leads.objects.all()
    context_object_name = 'leads'

    def get_context_data(self, **kwargs):

        user = self.request.user #atabekdemurtaza
        context = super(LeadListView, self).get_context_data(**kwargs)
        return context

#Old version
"""def lead_list(request):

    leads = Leads.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead-list.html', context)
"""
#New version
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    
    template_name = 'leads/lead-detail.html'
    context_object_name = 'lead'
    queryset = Leads.objects.all()

#Old version
"""def lead_detail(request, pk):

    lead = Leads.objects.get(id=pk)
    context = {
        'lead': lead        
    }
    return render(request, 'leads/lead-detail.html', context)
"""

#New version
class LeadCreateView(LoginRequiredMixin, generic.CreateView):

    template_name = 'leads/lead-create.html'
    form_class = LeadModelCreateForm
    #success_url = reverse_lazy('leads:lead_list')

    def get_success_url(self):
        return reverse('leads:lead_list')

    def form_valid(self, form):

        lead = form.save(commit=False)
        lead.save()
        #TO DO send mail
        send_mail(
            subject='A lead has been created already.',
            message='Go to the web site',
            from_email='atabekdemurtaza@gmail.com',
            recipient_list=['testuser@gmail.com']
        )
        return super(LeadCreateView, self).form_valid(form)



#Old version
"""def lead_create(request):

    #New version
    form = LeadModelCreateForm
    if request.method == "POST":
        form = LeadModelCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:lead_list')
    context = {
        'form': form
    }
    return render(request, 'leads/lead-create.html', context)
"""
def lead_delete(request, pk):

    lead = Leads.objects.get(id=pk)
    lead.delete()
    return redirect('leads:lead_list')

def lead_update(request, pk):

    #New version
    lead = Leads.objects.get(id=pk)
    form = LeadModelCreateForm(instance=lead)
    if request.method == "POST":
        form = LeadModelCreateForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('leads:lead_list')
    context = {
        'form': form
    }
    print(form)
    return render(request, 'leads/lead-create.html', context)

class LandingPageView(TemplateView):

    template_name = 'leads/landing-page.html'
