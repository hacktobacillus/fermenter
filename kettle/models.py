from django.db import models

class Drinker(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # It's a hackathon, screw passwords, this isn't prod
    likes = models.TextField()
    dislikes = models.TextField()
