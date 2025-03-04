from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ActionViewSet, TopicViewSet,
    action_list_view, add_action, edit_action, delete_action,
    get_actions, get_user_status, user_login_api, user_logout_api,
    user_login, user_logout
)

router = DefaultRouter()
router.register(r'actions', ActionViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path("actions/", action_list_view, name="action_list"),
    path("add_action/", add_action, name="add_action"),
    path("edit_action/<int:action_id>/", edit_action, name="edit_action"),
    path("delete_action/<int:action_id>/", delete_action, name="delete_action"),
    
    # ✅ API 端點
    path("api/actions/", get_actions, name="get_actions"),
    path("api/user_status/", get_user_status, name="user_status"),
    path("api/login/", user_login_api, name="login_api"),
    path("api/logout/", user_logout_api, name="logout_api"),
    path("api/", include(router.urls)),  # REST API
]
