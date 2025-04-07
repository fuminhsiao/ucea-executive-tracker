from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Action, Topic, ActionClick, Visit
from rest_framework import viewsets
from .serializers import ActionSerializer, TopicSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
import json
import logging

logger = logging.getLogger(__name__)

# ✅ API ViewSets
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

# ✅ 行動詳細頁
def action_detail(request, action_id):
    action = get_object_or_404(Action, id=action_id)
    return render(request, 'action_detail.html', {'action': action})

# ✅ 主頁 + 點擊數統計
def action_list_view(request):
    actions = Action.objects.all().order_by('-date')
    topics = Topic.objects.all()

    # 點擊統計
    click_data = (
        ActionClick.objects
        .values('action')
        .annotate(count=Count('id'))
    )
    click_dict = {item['action']: item['count'] for item in click_data}
    total_clicks = sum(click_dict.values())

    # ✅ 把點擊數塞進每個 action 物件
    for action in actions:
        action.click_count = click_dict.get(action.id, 0)

    return render(request, 'actions.html', {
        'actions': actions,
        'topics': topics,
        'total_clicks': total_clicks,
    })


# ✅ 登入／登出
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("action_list")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("action_list")

# ✅ 新增行動
@login_required
def add_action(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name_of_action")
            date = request.POST.get("date")
            description = request.POST.get("description")
            meaning = request.POST.get("meaning", "")
            source = request.POST.get("source", "")
            selected_topics = request.POST.getlist("topics")

            if not name or not date or not description:
                return render(request, "add_action.html", {
                    "error": "Please fill in all required fields.",
                    "topics": Topic.objects.all()
                })

            action = Action.objects.create(
                name_of_action=name,
                date=date,
                description=description,
                meaning=meaning,
                source=source
            )
            action.topics.set(selected_topics)

            return redirect("action_list")

        except Exception as e:
            return render(request, "add_action.html", {
                "error": str(e),
                "topics": Topic.objects.all()
            })

    return render(request, "add_action.html", {"topics": Topic.objects.all()})

# ✅ 編輯行動
@login_required
def edit_action(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == "POST":
        try:
            action.name_of_action = request.POST.get("name_of_action")
            action.date = request.POST.get("date")
            action.description = request.POST.get("description")
            action.meaning = request.POST.get("meaning", "")
            action.source = request.POST.get("source", "")
            selected_topics = request.POST.getlist("topics")

            if not action.name_of_action or not action.date or not action.description:
                return render(request, "edit_action.html", {
                    "error": "Please fill in all required fields.",
                    "action": action,
                    "topics": Topic.objects.all()
                })

            action.save()
            action.topics.set(selected_topics)
            return redirect("action_list")

        except Exception as e:
            return render(request, "edit_action.html", {
                "error": str(e),
                "action": action,
                "topics": Topic.objects.all()
            })

    return render(request, "edit_action.html", {
        "action": action,
        "topics": Topic.objects.all()
    })

# ✅ 刪除行動
@login_required
def delete_action(request, action_id):
    action = get_object_or_404(Action, id=action_id)
    action.delete()
    return redirect("action_list")

# ✅ 點擊追蹤 API
@csrf_exempt
def log_click(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action_id = data.get('action_id')
            action = Action.objects.get(id=action_id)
            ActionClick.objects.create(action=action)
            return JsonResponse({'status': 'ok'})
        except (json.JSONDecodeError, Action.DoesNotExist):
            return JsonResponse({'status': 'invalid data'}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=405)




@csrf_exempt
def record_visit(request):
    if request.method == 'POST':
        visit, _ = Visit.objects.get_or_create(id=1)
        visit.total_visits += 1
        visit.save()
        return JsonResponse({"status": "success", "total_visits": visit.total_visits})
    return JsonResponse({"status": "invalid request"}, status=405)