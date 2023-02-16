from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('profile/', views.profile, name="profile"),

    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('originals/<str:photo_name>', views.originals, name="originals"),
    path('originals/thumbs/<str:photo_name>', views.originals_thumbs, name="originals_thumbs"),
    path('delete/<str:photo_pk>', views.delete_image, name="delete"),

    path('thumbs/<str:photo_name>', views.thumbs_open, name="thumbs"),
    path('e/<str:expires_link>', views.expires_link_open, name="expires-link-open"),
]






