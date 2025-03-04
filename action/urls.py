from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActionViewSet, TopicViewSet

router = DefaultRouter()
router.register(r'actions', ActionViewSet)  # 註冊 API
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # 確保 API 路由啟用
]
