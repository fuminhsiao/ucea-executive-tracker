from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.apps import apps  # **這裡導入 apps**

class ActionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'action'

    def ready(self):
        post_migrate.connect(create_default_topics, sender=self)

def create_default_topics(sender, **kwargs):
    Topic = apps.get_model('action', 'Topic')  # **這裡的 apps 已正確導入**

    TOPIC_CHOICES = [
        "Research Funding", "DEI", "LGBTQ+", "School Choice", "Federal Workforce", 
        "Title IX", "Civil Rights", "Antisemitism", "Program Funding", "Regulations", 
        "Immigration", "Curriculum", "Healthcare", "Academic Freedom", 
        "PK-12 School Funding", "Postsecondary Funding", "Postsecondary", 
        "PK-12 Schools", "Department of Education", "State Jurisdiction", "International Education"
    ]

    for topic in TOPIC_CHOICES:
        Topic.objects.get_or_create(name=topic)
