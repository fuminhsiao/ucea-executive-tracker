from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('action.urls')),  # 確保 action 應用的 API 可用
]
