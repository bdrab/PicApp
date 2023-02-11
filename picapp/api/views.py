from rest_framework import generics, authentication

from website.models import Image
from website.serializers import ImageSerializer

from .permissions import IsStaffEditorPermission
from .authentication import CustomTokenAuthentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [authentication.SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsStaffEditorPermission]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

product_list_create_view = ProductListCreateAPIView.as_view()
