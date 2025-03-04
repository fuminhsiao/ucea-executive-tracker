from django.contrib import admin
from .models import Action, Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)  # 只顯示 Topic 名稱
    search_fields = ("name",)  # 支援搜尋功能

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("date", "name_of_action", "description", "source")  # 顯示主要欄位
    search_fields = ("name_of_action", "description", "meaning")  # 支援搜尋
    list_filter = ("topics", "date")  # 提供過濾器
