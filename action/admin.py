from django.contrib import admin
from .models import Action, Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)  # 只顯示 Topic 名稱
    search_fields = ("name",)  # 支援搜尋功能

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name_of_action', 'date', 'description')
    filter_horizontal = ('topics',)  # ✅ 讓 Topic 變成可勾選選項

admin.site.register(Action, ActionAdmin)
admin.site.register(Topic)
