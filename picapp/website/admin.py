from django.contrib import admin
from website.models import Tier, Image, ExpiresLink, ThumbnailImage, Profile
# Register your models here.

admin.site.register(Image)
admin.site.register(Tier)
admin.site.register(ExpiresLink)
admin.site.register(ThumbnailImage)
admin.site.register(Profile)