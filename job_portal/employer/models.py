from django.db import models
from django.conf import settings
from users.models import User

from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.timezone import now

class Vacancy(models.Model):
    WORK_MODE_CHOICES = [
        ('on_site', 'On Site'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]
    QUALIFICATION_CHOICES = [
        ('anyone', 'Anyone'),
        ('tenth', 'Tenth'),
        ('diploma/twelfth', 'Diploma/Twelfth'),
        ('graduation', 'Graduation'),
        ('postgraduation', 'Post Graduation')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacancies')
    company = models.CharField(max_length=100, blank=True, null = True)  # `null=True` removed
    role = models.CharField(max_length=50, default="Employee")

    description = models.TextField()
    resume_required = models.BooleanField(default=False, help_text="Indicates if a resume is required for the application.")

    location = models.CharField(max_length=50, blank=True, null = True)  
    work_mode = models.CharField(
        max_length=10,
        choices=WORK_MODE_CHOICES,
        default='on_site',
        help_text="Work mode for the vacancy."
    )
    experience = models.PositiveIntegerField(default=0)
    qualification = models.CharField(
        max_length=20,
        choices=QUALIFICATION_CHOICES,
        default='anyone'    
    )
    total_openings = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],  # Ensures at least 1 opening
        help_text="Number of available positions."
    )
    expire_date = models.DateField(
        blank=True, null=True,
        validators=[MinValueValidator(now().date())],  # Ensures future date
        help_text="Last date for applications."
    )

    def save(self, *args, **kwargs):
        # Auto-fill location from employer profile if not provided
        if not self.location and hasattr(self.user, 'employer_profile') and self.user.employer_profile.location:
            self.location = self.user.employer_profile.location
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role} at {self.company or 'Unknown'}"

