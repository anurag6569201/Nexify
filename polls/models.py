from django.db import models
from django.utils import timezone
from datetime import timedelta

# Function to calculate 30 minutes from now
def poll_close_time():
    return timezone.now() + timedelta(minutes=30)

class PollSet(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(default=poll_close_time)  # The time when poll closes

    def is_closed(self):
        return self.closed_at <= timezone.now()

    def time_remaining(self):
        return self.closed_at - timezone.now()

    def __str__(self):
        return self.title

class PollOption(models.Model):
    poll = models.ForeignKey(PollSet, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text