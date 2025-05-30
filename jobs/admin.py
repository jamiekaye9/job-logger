from django.contrib import admin
from .models import JobApplication, Stage, ApplicationNote, StageNote

admin.site.register(JobApplication)
admin.site.register(Stage)
admin.site.register(ApplicationNote)
admin.site.register(StageNote)

# Register your models here.
