from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    date = models.DateField()
    name_of_action = models.CharField(max_length=255)
    topics = models.ManyToManyField(Topic, related_name="actions")
    description = models.TextField()
    meaning = models.TextField()
    source = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name_of_action
