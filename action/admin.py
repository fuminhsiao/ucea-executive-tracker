from django.contrib import admin
from .models import Action, Topic, Actor, TypeOfAction

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(TypeOfAction)
class TypeOfActionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name_of_action', 'date', 'description')
    filter_horizontal = ('topics', 'type_of_action', 'actors')  # ✅ 多對多欄位用橫向選取器更好用
    search_fields = ('name_of_action', 'description')
    list_filter = ('date', 'status')  # ✅ 可以依時間和狀態過濾
