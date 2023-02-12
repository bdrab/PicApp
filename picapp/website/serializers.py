from rest_framework import serializers
from website.models import Image, ThumbnailImage, ExpiresLink
from django.contrib.auth.models import User



class ExpiresLinkSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField(read_only=True)
    image = serializers.CharField()
    time = serializers.IntegerField()
    class Meta:
        model = ExpiresLink
        fields = [
            'image',
            'time',
            'link',
        ]

    def get_image(self, obj):
        return obj.image.id

    def get_time(self, obj):
        return obj.time

    def get_link(self, obj):
        return obj.link

    def create(self, validated_data):
        image = Image.objects.all().filter(id=validated_data["image"]).first()
        owner = User.objects.all().filter(username=self.context["request"].user).first()
        time = validated_data["time"]
        expires_link = ExpiresLink.objects.create(image=image, time=time, owner=owner)

        return expires_link



class ImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    extension = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    thumbnails = serializers.SerializerMethodField(read_only=True)

    photo = serializers.ImageField(source="original")
    class Meta:
        model = Image
        fields = [
            'name',
            'extension',
            'photo',
            'thumbnail',
            'owner',
            'thumbnails',
        ]

    def get_name(self, obj):
        return obj.name

    def get_extension(self, obj):
        return obj.extension

    def get_thumbnail(self, obj):
        return f"http://192.168.0.136/{str(obj.thumbnail)}"

    def get_owner(self, obj):
        return obj.owner.username

    def get_thumbnails(self, obj):
        thumbs_links = []
        thumbs = ThumbnailImage.objects.all().filter(owner=obj.owner).filter(img=obj)
        for thumb in thumbs:
            thumbs_links.append(f"http://192.168.0.136/thumbs/{thumb.thumbnail}")
        return thumbs_links
