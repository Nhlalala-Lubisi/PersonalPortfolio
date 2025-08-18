from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=200, help_text='Comma-separated technologies')
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=120)
    date_earned = models.DateField()
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.issuer}"

class ProgrammingLanguage(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    name = models.CharField(max_length=60, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')

    def __str__(self):
        return f"{self.name} ({self.level})"
