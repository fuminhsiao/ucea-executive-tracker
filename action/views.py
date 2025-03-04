from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Action, Topic
from .serializers import ActionSerializer, TopicSerializer
import json
import logging

logger = logging.getLogger(__name__)

def action_list_view(request):
    actions = Action.objects.all()
    return render(request, "actions.html", {"actions": actions, "user": request.user})

# ✅ API：提供所有 Topics
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

# ✅ API：提供所有 Actions
class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

# ✅ API：提供所有 Actions (純 JSON)
def get_actions(request):
    actions = list(Action.objects.all().values(
        "id", "date", "name_of_action", "description", "meaning", "source"
    ))
    return JsonResponse(actions, safe=False)

# ✅ API：檢查使用者登入狀態
def get_user_status(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})

# ✅ API：登入
@csrf_exempt
def user_login_api(request):
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

# ✅ API：登出
@csrf_exempt
def user_logout_api(request):
    logout(request)
    return JsonResponse({"success": True})

# ✅ Django: 渲染 Actions 頁面
def action_list_view(request):
    actions = Action.objects.all()
    return render(request, "actions.html", {"actions": actions, "user": request.user})

# ✅ Django: 渲染登入頁面
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("action_list")
        return render(request, "login.html", {"error": "Invalid username or password!"})
    return render(request, "login.html")

# ✅ Django: 登出
def user_logout(request):
    logout(request)
    return redirect("action_list")

# ✅ API & Django: 新增 Action
@csrf_exempt
@login_required
def add_action(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST

            action = Action.objects.create(
                name_of_action=data["name_of_action"],
                date=data["date"],
                description=data["description"],
                meaning=data.get("meaning", ""),
                source=data.get("source", "")
            )
            if request.content_type == "application/json":
                return JsonResponse({"success": True, "id": action.id})
            return redirect("action_list")
        except Exception as e:
            logger.error(f"Error adding action: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return render(request, "add_action.html")

# ✅ API & Django: 編輯 Action
@csrf_exempt
@login_required
def edit_action(request, action_id):
    action = Action.objects.get(id=action_id)
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST

            action.name_of_action = data["name_of_action"]
            action.date = data["date"]
            action.description = data["description"]
            action.meaning = data.get("meaning", "")
            action.source = data.get("source", "")
            action.save()

            if request.content_type == "application/json":
                return JsonResponse({"success": True})
            return redirect("action_list")
        except Exception as e:
            logger.error(f"Error editing action: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return render(request, "edit_action.html", {"action": action})

# ✅ API & Django: 刪除 Action
@csrf_exempt
@login_required
def delete_action(request, action_id):
    if request.method == "DELETE":
        try:
            action = Action.objects.get(id=action_id)
            action.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            logger.error(f"Error deleting action: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
