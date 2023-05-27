from .serializers import (
    UserSerializer
)
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny
)

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    lookup_field = 'id'
