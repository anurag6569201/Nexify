from django.contrib import admin
from tracking import models

admin.site.register(models.FileUpload)
admin.site.register(models.FileMovement)
