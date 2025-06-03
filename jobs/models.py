from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_applied = models.DateField()
    date_updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('In Progress', 'In Progress'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
        ('Accepted', 'Accepted'),
    ])
    current_stage = models.ForeignKey('Stage', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} - {self.user.username}"

class Stage(models.Model):
    job_application = models.ForeignKey(JobApplication, related_name='stages', on_delete=models.CASCADE, null=True, blank=True)
    stage_number = models.IntegerField()
    stage_name = models.CharField(max_length=100)
    stage_date_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ])

    def __str__(self):
       if self.job_application:
           return f"Stage {self.stage_number} for {self.job_application.job_title} at {self.job_application.company_name}"
       else:
           return f"Stage {self.stage_number} (no job application)"

class ApplicationNote(models.Model):
    job_application = models.ForeignKey(JobApplication, related_name='notes', on_delete=models.CASCADE)
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note for {self.job_application.job_title} at {self.job_application.company_name}"
    
class StageNote(models.Model):
    stage = models.ForeignKey(Stage, related_name='notes', on_delete=models.CASCADE)
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note for {self.stage.stage_name} at {self.stage.job_application.company_name}"
