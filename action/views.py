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
    actions = Action.objects.all().order_by('-date')  # 確保按照日期排序
    topics = Topic.objects.all()  # 獲取所有 Topic
    return render(request, "actions.html", {"actions": actions, "topics": topics})

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Action, Topic

@login_required
def add_action(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name_of_action")
            date = request.POST.get("date")
            description = request.POST.get("description")
            meaning = request.POST.get("meaning", "")
            source = request.POST.get("source", "")
            selected_topics = request.POST.getlist("topics")  # Get multiple topics

            if not name or not date or not description:
                return render(request, "add_action.html", {"error": "Please fill in all required fields.", "topics": Topic.objects.all()})

            action = Action.objects.create(
                name_of_action=name, date=date, description=description, meaning=meaning, source=source
            )

            action.topics.set(selected_topics)  # Assign topics to action
            return redirect("action_list")

        except Exception as e:
            return render(request, "add_action.html", {"error": str(e), "topics": Topic.objects.all()})

    return render(request, "add_action.html", {"topics": Topic.objects.all()})


@login_required
def edit_action(request, action_id):
    action = Action.objects.get(id=action_id)

    if request.method == "POST":
        try:
            name = request.POST.get("name_of_action")
            date = request.POST.get("date")
            description = request.POST.get("description")
            meaning = request.POST.get("meaning", "")
            source = request.POST.get("source", "")
            selected_topics = request.POST.getlist("topics")  # Get selected topics (multiple)

            if not name or not date or not description:
                return render(request, "edit_action.html", {
                    "error": "Please fill in all required fields.",
                    "action": action,
                    "topics": Topic.objects.all()
                })

            # Update Action fields
            action.name_of_action = name
            action.date = date
            action.description = description
            action.meaning = meaning
            action.source = source
            action.save()

            # Update ManyToManyField (Topics)
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

@login_required
def delete_action(request, action_id):
    action = Action.objects.get(id=action_id)
    action.delete()
    return redirect("action_list")
