from django.db import models
from accounts.models import StudentProfile
from accounts.models import *

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=255, help_text="Comma-separated list of technologies")
    repo_link = models.URLField(blank=True)
    project_file = models.FileField(upload_to='projects/', blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Research(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='researches')
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    publication_link = models.URLField(blank=True)
    document = models.FileField(upload_to='research_papers/', blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='internships')
    organization = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    summary = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='client_favorites')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'student')

    def __str__(self):
        return f"{self.user.email} → {self.student.matric_number}"
    

class Notification(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.student:
            target = f"{self.student.registry.matric_number}"
        elif self.client:
            target = f"{self.client.user.email}"
        else:
            target = "Unknown"
        return f"Notification for {target}: {self.message[:30]}"