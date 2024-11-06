from django.db import models
from django.contrib.auth.models import User

class ClubData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fixed_json_metadata=models.TextField(default='"class": "go.TreeModel","nodeDataArray":',blank=True,null=True)
    json_data = models.TextField(default='{"class": "go.TreeModel", "nodeDataArray": []}',)

    def __str__(self):
        return str(self.json_data)
