from django.contrib import admin
from club import models

admin.site.register(models.ClubData)
admin.site.register(models.ClubDetails)
admin.site.register(models.ClubMember)
admin.site.register(models.ClubJoinRequest)
admin.site.register(models.MemberAddingRequests)
