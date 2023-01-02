from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('originals/<str:photo_name>', views.originals, name="originals"),
    path('originals/thumbs/<str:photo_name>', views.originals_thumbs, name="originals_thumbs"),
    path('thumbs/<str:photo_name>', views.thumbs, name="thumbs"),
    path('delete/<str:photo_pk>', views.delete, name="delete"),
    path('exp-link/<str:photo_pk>', views.expires_link_generate, name="expires-link-generate"),
    path('e/<str:expires_link>', views.expires_link_open, name="expires-link-open")
]





