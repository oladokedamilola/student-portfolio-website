from django.db import models
from django.utils import timezone
from accounts.models import StudentProfile, ClientProfile, User

class ChatThread(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='chat_threads')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='chat_threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.client.first_name} and {self.student.registry.first_name}"

class Message(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # sender can be client or student
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.timestamp}"
