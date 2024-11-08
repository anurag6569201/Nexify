from django.contrib import admin
from .models import PollSet, PollOption

admin.site.register(PollSet)
admin.site.register(PollOption)
