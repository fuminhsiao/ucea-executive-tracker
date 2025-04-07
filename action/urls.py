from django.urls import path, include
from .views import action_list_view, user_login, user_logout, add_action, edit_action, delete_action, action_detail, log_click, record_visit
from rest_framework.routers import DefaultRouter
from .views import ActionViewSet, TopicViewSet

router = DefaultRouter()
router.register(r'actions', ActionViewSet)  # ✅ 註冊 API 路由
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path("actions/", action_list_view, name="action_list"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("add_action/", add_action, name="add_action"),
    path("edit_action/<int:action_id>/", edit_action, name="edit_action"),
    path("delete_action/<int:action_id>/", delete_action, name="delete_action"),
    path('api/', include(router.urls)),
    path('actions/<int:action_id>/', action_detail, name='action_detail'),  # ✅ 新增 Action 詳細頁面
    path('api/log-click/', log_click, name='log_click'),
    path('api/record-visit/', record_visit, name='record_visit'),

]
