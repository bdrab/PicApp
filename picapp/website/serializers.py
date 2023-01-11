from rest_framework import serializers
from website.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'name',
            'extension',
            'original',
            'thumbnail',
            'owner',
        ]