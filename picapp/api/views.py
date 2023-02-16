from rest_framework import generics, authentication

from website.models import Image, ExpiresLink
from website.serializers import ImageSerializer, ExpiresLinkSerializer, ImageSerializerExclusive

from .permissions import IsStaffEditorPermission
from .authentication import CustomTokenAuthentication

from rest_framework.response import Response
from rest_framework import status

from django.http import QueryDict


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [authentication.SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsStaffEditorPermission]

    def create(self, request, *args, **kwargs):
        element_list = request.data.getlist("photo")
        many_val = False
        data = request.data
        if len(request.data.getlist("photo")) > 1:
            many_val = True
            data = []
            query_dict = QueryDict('', mutable=True)

            for element in element_list:
                ordinary_dict = {'photo': element}
                query_dict.update(ordinary_dict)
                data.append(query_dict)

        serializer = self.get_serializer(data=data, many=many_val)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.request.user.profile.tier.name == "Exclusive":
            return ImageSerializerExclusive
        else:
            return ImageSerializer

product_list_create_view = ProductListCreateAPIView.as_view()


class ExpiresLinkCreateAPIView(generics.CreateAPIView):
    queryset = ExpiresLink.objects.all()
    serializer_class = ExpiresLinkSerializer
    authentication_classes = [authentication.SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsStaffEditorPermission]

expires_link_create_view = ExpiresLinkCreateAPIView.as_view()