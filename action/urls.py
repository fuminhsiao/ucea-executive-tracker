from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActionViewSet, TopicViewSet, action_list_view, get_actions, get_user_status, user_login, user_logout

router = DefaultRouter()
router.register(r'actions', ActionViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path("api/actions/", get_actions, name="get_actions"),
    path("api/user_status/", get_user_status, name="user_status"),
    path("api/login/", user_login, name="login"),
    path("api/logout/", user_logout, name="logout"),
    path("api/", include(router.urls)),  # ✅ 確保 API 仍然可以運作
    path("actions/", action_list_view, name="action_list"),
]
