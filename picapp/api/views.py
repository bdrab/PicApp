from rest_framework import generics, authentication

from website.models import Image, ExpiresLink
from website.serializers import ImageSerializer, ExpiresLinkSerializer

from .permissions import IsStaffEditorPermission
from .authentication import CustomTokenAuthentication

#
# from rest_framework.parsers import MultiPartParser, FormParser
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # parser_classes = (MultiPartParser, FormParser,)
    authentication_classes = [authentication.SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsStaffEditorPermission]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

product_list_create_view = ProductListCreateAPIView.as_view()


class ExpiresLinkCreateAPIView(generics.CreateAPIView):
    queryset = ExpiresLink.objects.all()
    serializer_class = ExpiresLinkSerializer
    authentication_classes = [authentication.SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsStaffEditorPermission]

expires_link_create_view = ExpiresLinkCreateAPIView.as_view()