import json
from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from website.models import Image, ExpiresLink, ThumbnailImage
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse, JsonResponse
import time


# TODO: if image bigger than 4MB is selected is still possible to be sent to server,
#  even if it is not shown below the drop zone.
@csrf_exempt
def index(request):
    if request.method == "POST":
        for file in request.FILES.getlist("files"):
            try:
                if request.user.is_authenticated:
                    owner = User.objects.get(username=request.user)
                else:
                    owner = User.objects.get(pk=request.POST.get("user"))
                image = Image(owner=owner, original=file)
                image.save(size=(300, 600))
            except Exception as e:
                print(e)
                messages.error(request, 'UPLOAD. Upload failed.')
        messages.info(request, 'UPLOAD. Successful')
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


def originals(request, photo_name):
    if request.user.is_authenticated:
        img = Image.objects.get(original="originals/"+photo_name)
        if img.owner == request.user:
            return FileResponse(img.original.open(), as_attachment=True)
    return redirect("index")


def originals_thumbs(request, photo_name):
    if request.user.is_authenticated:
        img = Image.objects.get(thumbnail="originals/thumbs/"+photo_name)
        if img.owner == request.user:
            return FileResponse(img.thumbnail.open(), as_attachment=True)
    return redirect("index")

def thumbs(request, photo_name):
    try:
        thumb = ThumbnailImage.objects.get(thumbnail="thumbs/"+photo_name)
        return FileResponse(thumb.thumbnail.open(), as_attachment=True)
    except Exception:
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
        images = []
        new_images = Image.objects.all().filter(owner=User.objects.get(username=request.user))
        for new_image in new_images:
            thumbnail = ThumbnailImage.objects.select_related().filter(img = new_image.pk)
            images.append([new_image, thumbnail])
        context["user_photos"] = images
    return render(request, "website/profile.html", context=context)

@csrf_exempt
def expires_link_generate(request, photo_pk):
    response = {}
    data = json.loads(request.body)
    time_link = data["time"]
    if request.user.is_authenticated:
        new_link = ExpiresLink.objects.create(owner=User.objects.get(username=request.user),
                                              image=Image.objects.get(pk=photo_pk),
                                              time=time_link)
        response["web_address"] = f"http://192.168.0.136/e/{new_link.link}"
    return JsonResponse(response)


def expires_link_open(request, expires_link):
    try:
        expires_link = ExpiresLink.objects.get(link=expires_link)
    except Exception:
        return redirect("index")
    else:
        if expires_link.created.timestamp() + expires_link.time >= time.time():
            image = expires_link.image
            return FileResponse(image.original.open(), as_attachment=True)
    return redirect("index")
