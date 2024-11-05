from django.db import models
from django.contrib.auth.models import User

class ClubData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fixed_json_metadata=models.TextField(default='"class": "go.TreeModel","nodeDataArray":',blank=True,null=True)
    json_data = models.TextField(default='{"class": "go.TreeModel", "nodeDataArray": [{"key": 1, "name": "Stella Payne Diaz", "title": "CEO", "dept": "Management", "pic": "1.jpg", "email": "sdiaz@example.com", "phone": "(234) 555-6789"}]}',)

    def __str__(self):
        return str(self.json_data)
