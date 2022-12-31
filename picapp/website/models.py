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
    expiring_links = models.BooleanField(default=False)
    original_photo = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name) + "" + str(self.description)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     tier = models.ForeignKey(Tier, null=True, on_delete=models.SET_NULL)


# TODO: image is still open after creation and cannot be easily deleted.
# TODO: add delete function for image  thumbs
class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=20, default="name")
    extension = models.CharField(max_length=20, default="extension")
    original = models.ImageField(upload_to='originals/')
    thumbnail = models.ImageField(upload_to="originals/thumbs/")

    def delete(self, *args, **kwargs):
        os.remove(str(settings.BASE_DIR) + "\\" + self.original.name.replace("/", "\\"))
        os.remove(str(settings.BASE_DIR) + "\\" + self.thumbnail.name.replace("/", "\\"))
        thumbnails = ThumbnailImage.objects.all().filter(img=self)
        for thumbnail in thumbnails:
            os.remove(str(settings.BASE_DIR) + "\\" + thumbnail.thumbnail.name.replace("/", "\\"))
        super(Image, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        file = str(self.original).split(".")
        self.name = file[0]
        self.extension = file[1]

        super(Image, self).save()

        self.create_thumbnail((150, 150), True)
        if kwargs["size"]:
            sizes = kwargs["size"]
            for size in sizes:
                self.create_thumbnail((size, size))

        super(Image, self).save()


    def create_thumbnail(self, size, image_thumbnail = False):
        image = IM.open(str(self.original))
        image.thumbnail(size, IM.ANTIALIAS)

        thumb_extension = self.extension
        thumb_filename = self.name+f"_thumbs_{size[1]}."+self.extension

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

        if not image_thumbnail:
            ThumbnailImage.objects.create(owner= self.owner,
                                          img=self,
                                          size_height=size[1],
                                          thumbnail=ContentFile(temp_thumbnail.read(),
                                                                name=thumb_filename))
        else:
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumbnail.read()), save=False)
        temp_thumbnail.close()
        image.close()

class ThumbnailImage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    img = models.ForeignKey(Image, null=True, on_delete=models.CASCADE)
    size_height = models.IntegerField(blank=False, null=False)
    thumbnail = models.ImageField(upload_to='thumbs/', editable=True, default="none")


class ExpiresLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(blank=False, null=False)
    link = models.CharField(max_length=36, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        super(ExpiresLink, self).save(*args, **kwargs)
