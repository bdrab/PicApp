import json
from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from website.models import Image, ExpiresLink, ThumbnailImage, Tier
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse, JsonResponse
import time
from .forms import CreateProfileForm
from PIL import Image as IM
from io import BytesIO
from django.core.files.base import ContentFile


def index(request):
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
    form_profile = CreateProfileForm()
    context = {"form_register": form_register,
               "form_profile": form_profile}
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.instance.user = user
            profile_form.save()
            return redirect('index')

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
        thumb = ThumbnailImage.objects.get(thumbnail=photo_name)
        image_db = thumb.img
        size = (thumb.size_height, thumb.size_height)

        image = IM.open(str(image_db.original))
        image.thumbnail(size, IM.ANTIALIAS)

        thumb_extension = image_db.extension
        thumb_filename = image_db.name + f"_thumbs_{size[1]}." + image_db.extension

        if thumb_extension in ['jpg', 'jpeg']:
            file_type = 'JPEG'
        elif thumb_extension == 'gif':
            file_type = 'GIF'
        elif thumb_extension == 'png':
            file_type = 'PNG'
        else:
            file_type = ""

        temp_thumbnail = BytesIO()
        image.save(temp_thumbnail, file_type)
        temp_thumbnail.seek(0)
        file = ContentFile(temp_thumbnail.read(), name=thumb_filename)
        temp_thumbnail.close()
        image.close()

        return FileResponse(file.open(), as_attachment=True)

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
        user = User.objects.get(username=request.user)
        new_images = Image.objects.all().filter(owner=user)
        for new_image in new_images:
            thumbnail = ThumbnailImage.objects.select_related().filter(img = new_image.pk)
            images.append([new_image, thumbnail])
        context["user_photos"] = images
        context["user"] = user
    return render(request, "website/profile.html", context=context)


@csrf_exempt
def expires_link_generate(request, photo_pk):
    response = {}
    time_link = json.loads(request.body)["time"]
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if user.profile.tier.expiring_links:
            new_link = ExpiresLink.objects.create(owner=user,
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
