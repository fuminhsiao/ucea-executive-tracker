from django.urls import path, include
from .views import action_list_view, user_login, user_logout, add_action, edit_action, delete_action
from rest_framework.routers import DefaultRouter
from .views import (
    ActionViewSet, TopicViewSet, 
    get_actions, get_user_status, user_login, user_logout,
    add_action, edit_action, delete_action
)

router = DefaultRouter()
router.register(r'actions', ActionViewSet)
router.register(r'topics', TopicViewSet)
urlpatterns = [
    path("actions/", action_list_view, name="action_list"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("add_action/", add_action, name="add_action"),
    path("edit_action/<int:action_id>/", edit_action, name="edit_action"),
    path("delete_action/<int:action_id>/", delete_action, name="delete_action"),
    path("api/", include(router.urls)),
]
