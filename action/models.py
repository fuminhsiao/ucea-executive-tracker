from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Actor(models.Model):  
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class TypeOfAction(models.Model):  
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
    name_of_action = models.CharField(max_length=500)
    type_of_action = models.ManyToManyField(TypeOfAction, related_name="actions")
    actors = models.ManyToManyField(Actor, related_name="actions")
    topics = models.ManyToManyField(Topic, related_name="actions")
    description = models.TextField(null=True)
    meaning = models.TextField(blank=True, null=True)
    source = models.URLField(max_length=500, blank=True, null=True)

    status = models.CharField(max_length=500, blank=True, null=True)  
    challenge_to_action = models.TextField(blank=True, null=True)

    # ✅ 拆分 `news_commentary` 為標題 & 連結
    news_title = models.CharField(max_length=500, blank=True, null=True)  
    news_link = models.URLField(max_length=1000, blank=True, null=True)  

    notes = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    fallout = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name_of_action
