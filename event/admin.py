from django.contrib import admin


from event import models 
admin.site.register(models.Form)
admin.site.register(models.Option)
admin.site.register(models.Question)