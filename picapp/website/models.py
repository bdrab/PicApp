from django.db import models
from django.contrib.auth.models import User
from picapp import settings
from PIL import Image as IM
import os
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

class Tier(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + "" + str(self.description)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     tier = models.ForeignKey(Tier, null=True, on_delete=models.SET_NULL)


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    upload = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=20, default="name")
    extension = models.CharField(max_length=20, default="extension")
    thumbnail = models.ImageField(upload_to='thumbs/', editable=False, default="none")

    def delete(self, *args, **kwargs):
        os.remove(str(settings.BASE_DIR) + "\\" + self.upload.name.replace("/", "\\"))
        os.remove(str(settings.BASE_DIR) + "\\" + self.thumbnail.name.replace("/", "\\"))
        super(Image, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        file = str(self.upload).split(".")
        self.name = file[0]
        self.extension = file[1]
        if not self.create_thumbnail((500, 500)):
            raise Exception
        super(Image, self).save(*args, **kwargs)

    def create_thumbnail(self, size):
        image = IM.open(self.upload)
        image.thumbnail(size, IM.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.upload.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False


        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class ExpiresLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(blank=False, null=False)
    link = models.CharField(max_length=36, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        super(ExpiresLink, self).save(*args, **kwargs)
