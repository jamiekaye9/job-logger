from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from jobs.views import HomeView, SignupView, CustomLoginView, CustomLogoutView, ProfileView, JobApplicationListView, JobApplicationCreateView, JobApplicationDetailView, JobApplicationUpdateView, JobApplicationDeleteView, StageCreateView, StageDetailView, StageUpdateView, StageDeleteView, ApplicationNoteCreateView, StageNoteCreateView, ApplicationNoteUpdateView, StageNoteUpdateView, ApplicationNoteDeleteView, StageNoteDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('job_applications/', JobApplicationListView.as_view(), name='job_application_list'),
    path('new_job_application/', JobApplicationCreateView.as_view(), name='job_application_form'),
    path('job_applications/<int:pk>/', JobApplicationDetailView.as_view(), name='job_application_detail'),
    path('job_applications/<int:pk>/update/', JobApplicationUpdateView.as_view(), name='job_application_update'),
    path('job_applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='job_application_delete'),

    path('stages/new/<int:application_id>/', StageCreateView.as_view(), name='create_stage'),
    path('stages/<int:pk>/', StageDetailView.as_view(), name='stage_detail'),
    path('stages/<int:pk>/update/', StageUpdateView.as_view(), name='update_stage'),
    path('stages/<int:pk>/delete/', StageDeleteView.as_view(), name='delete_stage'),

    path('job_applications/<int:application_id>/add_note/', ApplicationNoteCreateView.as_view(), name='add_application_note'),
    path('stages/<int:stage_id>/add_note/', StageNoteCreateView.as_view(), name='add_stage_note'),
    path('job_applications/<int:application_id>/notes/<int:note_id>/update/', ApplicationNoteUpdateView.as_view(), name='update_application_note'),
    path('stages/<int:stage_id>/notes/<int:note_id>/update/', StageNoteUpdateView.as_view(), name='update_stage_note'),
    path('job_applications/<int:application_id>/notes/<int:note_id>/delete/', ApplicationNoteDeleteView.as_view(), name='delete_application_note'),
    path('stages/<int:stage_id>/notes/<int:note_id>/delete/', StageNoteDeleteView.as_view(), name='delete_stage_note'),
]