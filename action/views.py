from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Action, Topic

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
        name = request.POST["name_of_action"]
        date = request.POST["date"]
        description = request.POST["description"]
        meaning = request.POST["meaning"]
        source = request.POST["source"]
        
        action = Action.objects.create(
            name_of_action=name, date=date, description=description, meaning=meaning, source=source
        )
        return redirect("action_list")

@login_required
def edit_action(request, action_id):
    action = Action.objects.get(id=action_id)
    if request.method == "POST":
        action.name_of_action = request.POST["name_of_action"]
        action.date = request.POST["date"]
        action.description = request.POST["description"]
        action.meaning = request.POST["meaning"]
        action.source = request.POST["source"]
        action.save()
        return redirect("action_list")
    
    return render(request, "edit_action.html", {"action": action})

@login_required
def delete_action(request, action_id):
    action = Action.objects.get(id=action_id)
    action.delete()
    return redirect("action_list")
