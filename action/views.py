from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Action, Topic
import logging
from rest_framework import viewsets
from .models import Action, Topic
from .serializers import ActionSerializer, TopicSerializer
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    
logger = logging.getLogger(__name__)

def action_list_view(request):
    actions = Action.objects.all()
    return render(request, "actions.html", {"actions": actions, "user": request.user})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("action_list")  # 登入成功後重新導向
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("action_list")  # 登出後重新導向

@login_required
def add_action(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name_of_action")
            date = request.POST.get("date")
            description = request.POST.get("description")
            meaning = request.POST.get("meaning", "")
            source = request.POST.get("source", "")

            # ✅ 確保所有欄位都有值
            if not name or not date or not description:
                return render(request, "add_action.html", {"error": "請填寫所有必填欄位"})

            action = Action.objects.create(
                name_of_action=name, date=date, description=description, meaning=meaning, source=source
            )
            return redirect("action_list")  # ✅ 新增成功後，回到列表頁

        except Exception as e:
            logger.error(f"Error adding action: {str(e)}")
            return render(request, "add_action.html", {"error": str(e)})

    return render(request, "add_action.html")  # ✅ 處理 `GET` 請求時，顯示 `add_action.html`

@login_required
def edit_action(request, action_id):
    action = Action.objects.get(id=action_id)
    if request.method == "POST":
        try:
            action.name_of_action = request.POST.get("name_of_action")
            action.date = request.POST.get("date")
            action.description = request.POST.get("description")
            action.meaning = request.POST.get("meaning", "")
            action.source = request.POST.get("source", "")
            action.save()
            return redirect("action_list")
        except Exception as e:
            logger.error(f"Error editing action: {str(e)}")
            return render(request, "error.html", {"message": str(e)})
    
    return render(request, "edit_action.html", {"action": action})

@login_required
def delete_action(request, action_id):
    action = Action.objects.get(id=action_id)
    action.delete()
    return redirect("action_list")
