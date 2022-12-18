from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from website.models import Image
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse
from sorl.thumbnail import get_thumbnail

@csrf_exempt
def index(request):
    if request.method == "POST":
        print(request.FILES)
        for file in request.FILES.getlist("files"):
            try:
                if request.user.is_authenticated:
                    owner = User.objects.get(username=request.user)
                else:
                    owner = User.objects.get(pk=request.POST.get("user"))
                Image.objects.create(owner=owner, upload=file)
            except Exception as e:
                messages.error(request, 'UPLOAD. Upload failed.')

    return render(request, "website/index.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'LOGIN.User does not exist')
            return render(request, "website/login.html")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, 'LOGIN.Incorrect password')
        return render(request, "website/login.html")

    return render(request, "website/login.html")


def register(request):
    form_register = UserCreationForm()
    context = {"form_register": form_register}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    return render(request, "website/register.html", context=context)


def logout_user(request):
    logout(request)
    return redirect("index")


def uploads(request, photo_name):
    if request.user.is_authenticated:
        img = Image.objects.get(upload="uploads/"+photo_name)
        if img.owner == request.user:
            return FileResponse(img.upload.open(), as_attachment=True)
    return redirect("index")


def delete(request, photo_pk):
    if request.user.is_authenticated:
        img = Image.objects.get(pk=photo_pk)
        if img.owner == request.user:
            img.delete()
    return redirect("profile")


def profile(request):
    context = {}
    if request.user.is_authenticated:
        images = Image.objects.all().filter(owner=User.objects.get(username=request.user))
        context["user_photos"] = images
    return render(request, "website/profile.html", context=context)