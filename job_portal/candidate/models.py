from django.db import models
from users.models import *
from employer.models import * 
from django.conf import settings


# Create your models here.

class SavedJobs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    vacancies = models.ManyToManyField(Vacancy, related_name='saved_by_users')
    created_time = models.DateField(auto_now_add=True)


class Work(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "works")
    company = models.CharField(max_length = 40, blank = True, null = True)
    still_working = models.BooleanField(default = False)
    start_date = models.DateField()
    end_date = models.DateField()


    def save(self, *args, **kwargs):
        if self.still_working:
            self.end_date = None
        super().save(*args, **kwargs)


class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "education")
    college = models.CharField(max_length = 100)
    start_date = models.DateField()
    end_date = models.DateField()




class Application(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=[('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected')], default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)


class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume")
    resume_file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
