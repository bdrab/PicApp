from django.contrib import admin
from website.models import Tier, Image, ExpiresLink
# Register your models here.

admin.site.register(Image)
admin.site.register(Tier)
admin.site.register(ExpiresLink)
