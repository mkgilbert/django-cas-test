from django.db import models
from django.contrib.auth.models import User

class CVTUser(models.Model):
    user = models.OneToOneField(User)
    is_logged_in = models.BooleanField(default=False)
