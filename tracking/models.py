from django.db import models
from django.contrib.auth.models import User
import uuid

import uuid
from django.db import models
from django.contrib.auth.models import User

class FileUpload(models.Model):
    file_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploaded_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    short_note = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=40, choices=[
        ('Department', 'Department'),
        ('User', 'User'),
    ])

    def __str__(self):
        return f"File {self.file.name} uploaded by {self.uploaded_by.username}"


class FileMovement(models.Model):
    file = models.ForeignKey('FileUpload', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_files', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_files', on_delete=models.CASCADE)
    short_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='In Progress')  # 'In Progress', 'Received', 'Rejected'
    feedback = models.TextField(blank=True, null=True)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.file.file.name} from {self.sender.username} to {self.receiver.username}"