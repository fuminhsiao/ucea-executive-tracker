from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Actor(models.Model):  # ✅ Actor 仍為多對多
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    TYPE_OF_ACTION_CHOICES = [
        ('Executive Order', 'Executive Order'),
        ('Agency action', 'Agency action'),
        ('Litigation', 'Litigation'),
        ('Agency Memo/Letter', 'Agency Memo/Letter'),
        ('Nomination/Appointment', 'Nomination/Appointment'),
        ('Congressional Action', 'Congressional Action'),
        ('Court Ruling/Action', 'Court Ruling/Action'),
    ]

    date = models.DateField()
    name_of_action = models.CharField(max_length=255)
    type_of_action = models.CharField(max_length=50, choices=TYPE_OF_ACTION_CHOICES, default='Agency action', null=True)  # ✅ 改為 `CharField`
    actors = models.ManyToManyField(Actor, related_name="actions", null=True)  # ✅ 多對多
    topics = models.ManyToManyField(Topic, related_name="actions")
    description = models.TextField()
    meaning = models.TextField()
    source = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=255, blank=True, null=True)  
    challenge_to_action = models.TextField(blank=True, null=True)
    news_commentary = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    fallout = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name_of_action
