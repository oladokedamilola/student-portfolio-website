from django.db import models
from accounts.models import StudentProfile
from accounts.models import *


class Project(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=255, help_text="Comma-separated list of technologies")
    repo_link = models.URLField(blank=True)
    project_file = models.FileField(upload_to='projects/', blank=True)

    def __str__(self):
        return self.title


class Research(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='researches')
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    publication_link = models.URLField(blank=True)
    document = models.FileField(upload_to='research_papers/', blank=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='internships')
    organization = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)  # e.g. "June 2023 - Sept 2023"
    summary = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.organization}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'student')

    def __str__(self):
        return f"{self.user.email} → {self.student.matric_number}"
    

class Notification(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.student.matric_number}: {self.message[:30]}"