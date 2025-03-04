from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
import json
from .models import Action, Topic
from .serializers import ActionSerializer, TopicSerializer

# 🔹 保留 REST API 端點
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 未登入只能讀取

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 未登入只能讀取

# 🔹 API: 取得所有 Actions（前端用）
def get_actions(request):
    actions = Action.objects.all().values(
        "id", "date", "name_of_action", "description", "meaning", "source"
    )
    return JsonResponse(list(actions), safe=False)

# 🔹 API: 取得登入狀態
def get_user_status(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})

# 🔹 API: 登入
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                login(request, user)
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "message": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

# 🔹 API: 登出
@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({"success": True})

# 🔹 API: 新增 Action（登入後才可用）
@csrf_exempt
@login_required
def add_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = Action.objects.create(
                date=data["date"],
                name_of_action=data["name_of_action"],
                description=data["description"],
                meaning=data.get("meaning", ""),
                source=data.get("source", "")
            )
            if "topics" in data:
                topics = Topic.objects.filter(id__in=data["topics"])
                action.topics.set(topics)  # 設定 Topics
            return JsonResponse({"success": True, "id": action.id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

# 🔹 API: 編輯 Action（登入後才可用）
@csrf_exempt
@login_required
def edit_action(request, action_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = Action.objects.get(id=action_id)
            action.date = data["date"]
            action.name_of_action = data["name_of_action"]
            action.description = data["description"]
            action.meaning = data.get("meaning", "")
            action.source = data.get("source", "")
            action.save()

            if "topics" in data:
                topics = Topic.objects.filter(id__in=data["topics"])
                action.topics.set(topics)  # 更新 Topics

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

# 🔹 API: 刪除 Action（登入後才可用）
@csrf_exempt
@login_required
def delete_action(request, action_id):
    if request.method == "DELETE":
        try:
            action = Action.objects.get(id=action_id)
            action.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
