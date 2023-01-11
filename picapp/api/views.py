from website.models import Image
from website.serializers import ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def api_home(request, *args, **kwargs):
    instance = Image.objects.all().order_by("?").first()
    data = {}
    if instance:
        data = ImageSerializer(instance).data
    return Response(data)
