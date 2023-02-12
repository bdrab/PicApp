from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.product_list_create_view),
    path('createExpiresLink/', views.expires_link_create_view),
    path('auth/', obtain_auth_token)
]



