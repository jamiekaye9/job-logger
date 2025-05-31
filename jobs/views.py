from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from jobs.forms.forms import CustomUserCreationForm, JobApplicationForm, StageForm, ApplicationNoteForm, StageNoteForm
from django.contrib.auth import authenticate, login
from .models import JobApplication, Stage, ApplicationNote, StageNote

class HomeView(TemplateView):
    template_name = 'home/home.html'

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

class JobApplicationListView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'profile/job_application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'profile/job_application_form.html'
    success_url = reverse_lazy('job_application_list')

    def form_valid(self, form):
        job_application = form.save(commit=False)
        job_application.user = self.request.user
        job_application.save()
        return super().form_valid(form)

class JobApplicationDetailView(LoginRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'profile/job_application_detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            job_application = JobApplication.objects.get(pk=self.object.pk)
            context['stages'] = job_application.stages.all()
            context['stage_form'] = StageForm()
            context['note_form'] = ApplicationNoteForm()
            context['notes'] = job_application.notes.all()
            context['stage_notes'] = StageNote.objects.filter(stage__job_application=job_application)
            context['stage_note_form'] = StageNoteForm()
            
            editing_stage_id = self.request.GET.get("edit")
            context['editing_stage_id'] = int(editing_stage_id) if editing_stage_id else None
    
            if editing_stage_id:
                try:
                    stage = Stage.objects.get(id=editing_stage_id, job_application=job_application)
                    context['edit_stage_form'] = StageForm(instance=stage)
                except Stage.DoesNotExist:
                    context['edit_stage_form'] = None
            else:
                context['edit_stage_form'] = None

            context['current_stage'] = job_application.current_stage
            return context

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

class JobApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobApplication
    template_name = 'profile/job_application_form.html'
    context_object_name = 'application'
    fields = ['company_name', 'job_title', 'salary', 'location', 'date_applied', 'status']

    def get_success_url(self):
        return reverse_lazy('job_application_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        application = self.get_object()
        return application.user == self.request.user

class JobApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobApplication
    template_name = 'profile/job_application_confirm_delete.html'
    context_object_name = 'application'
    success_url = reverse_lazy('job_application_list')

    def test_func(self):
        application = self.get_object()
        return application.user == self.request.user

class StageCreateView(LoginRequiredMixin, CreateView):
    model = Stage
    template_name = 'profile/job_application_detail.html'
    fields = ['stage_name', 'stage_date_time', 'status']
    
    def form_valid(self, form):
        job_application_id = self.kwargs.get('application_id')
        job_application = JobApplication.objects.get(id=job_application_id, user=self.request.user)
        stage = form.save(commit=False)
        stage.job_application = job_application
        last_stage = job_application.stages.order_by('stage_number').last()
        stage.stage_number = last_stage.stage_number + 1 if last_stage else 1
        job_application.current_stage = stage
        stage.save()
        job_application.save()
        return redirect('job_application_detail', pk=job_application.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_application_id = self.kwargs.get('application_id')
        job_application = JobApplication.objects.get(id=job_application_id, user=self.request.user)
        context['application'] = job_application
        context['stages'] = job_application.stages.all()
        context['stage_form'] = StageForm()
        return context

class StageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stage
    form_class = StageForm
    template_name = 'profile/job_application_detail.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('job_application_detail', pk=self.object.job_application.pk)

    def get_success_url(self):
        return reverse_lazy('job_application_detail', kwargs={'pk': self.object.job_application.pk})

    def test_func(self):
        return self.get_object().job_application.user == self.request.user

class StageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Stage
    template_name = 'profile/stage_confirm_delete.html'
    context_object_name = 'stage'

    def form_valid(self, form):
        self.object = self.get_object()
        job_application = self.object.job_application
        is_current_stage = (job_application.current_stage_id == self.object.id)

        new_current_stage = None
        if is_current_stage:
            remaining_stages = job_application.stages.exclude(id=self.object.id).order_by('-stage_number')
            new_current_stage = remaining_stages.first()

        self.object.delete()

        if is_current_stage:
            job_application.current_stage = new_current_stage
            job_application.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('job_application_detail', kwargs={'pk': self.object.job_application.pk})

    def test_func(self):
        stage = self.get_object()
        return stage.job_application.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.object.job_application
        return context

class ApplicationNoteCreateView(LoginRequiredMixin, CreateView):
    model = ApplicationNote
    fields = ['note_text']
    template_name = 'profile/job_application_detail.html'

    def form_valid(self, form):
        form.instance.job_application = get_object_or_404(JobApplication, pk=self.kwargs['application_id'], user=self.request.user)
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job_application_detail', kwargs={'pk': self.object.job_application.pk})

class StageNoteCreateView(LoginRequiredMixin, CreateView):
    model = StageNote
    fields = ['note_text']
    template_name = 'profile/job_application_detail.html'

    def form_valid(self, form):
        stage = get_object_or_404(Stage, pk=self.kwargs['stage_id'], job_application__user=self.request.user)
        form.instance.stage = stage
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job_application_detail', kwargs={'pk': self.object.stage.job_application.pk})