from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.apps import apps  # ✅ 確保 `apps` 被正確導入

class ActionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'action'

    def ready(self):
        # ✅ `post_migrate` 會在 `migrate` 完成後執行，確保預設資料被建立
        post_migrate.connect(create_default_data, sender=self)

def create_default_data(sender, **kwargs):
    """ 在 `migrate` 後自動建立 `Topic`、`TypeOfAction`、`Actor` 預設值 """

    # ✅ 取得模型
    Topic = apps.get_model('action', 'Topic')
    TypeOfAction = apps.get_model('action', 'TypeOfAction')
    Actor = apps.get_model('action', 'Actor')

    # ✅ 預設 `Topic` 清單
    TOPIC_CHOICES = [
        "Research Funding", "DEI", "LGBTQ+", "School Choice", "Federal Workforce", 
        "Title IX", "Civil Rights", "Antisemitism", "Program Funding", "Regulations", 
        "Immigration", "Curriculum", "Healthcare", "Academic Freedom", 
        "PK-12 School Funding", "Postsecondary Funding", "Postsecondary", 
        "PK-12 Schools", "Department of Education", "State Jurisdiction", "International Education", "Governance", "Early Childhood",
        "Educator Workforce"
    ]

    # ✅ 預設 `TypeOfAction` 清單
    TYPE_OF_ACTION_CHOICES = [
        "Executive Order", "Agency action", "Litigation", "Agency Memo/Letter",
        "Nomination/Appointment", "Congressional Action", "Court Ruling/Action"
    ]

    # ✅ 更新 `Actor` 預設清單
    ACTOR_CHOICES = [
        "Dept of Ed", "POTUS", "DOGE", "HHS", "OMB",
        "Office of Personnel Management", "NIH", "DoD", "U.S. Congress", "SCOTUS",
        "Dept of Agriculture", "Dept of Interior", "USAID", 
        "Department of Labor", "Department of Justice", "NOAA", "NRLB", "Department of State",
        "Federal Court"
    ]

    # ✅ 批量導入 `Topic`
    for topic in TOPIC_CHOICES:
        Topic.objects.get_or_create(name=topic)

    # ✅ 批量導入 `TypeOfAction`
    for action_type in TYPE_OF_ACTION_CHOICES:
        TypeOfAction.objects.get_or_create(name=action_type)

    # ✅ 批量導入 `Actor`
    for actor in ACTOR_CHOICES:
        Actor.objects.get_or_create(name=actor)

    print("✅ 預設 `Topic`、`TypeOfAction`、`Actor` 已成功導入！")
