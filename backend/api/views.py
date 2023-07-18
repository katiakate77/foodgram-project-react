from rest_framework import viewsets

from api.serializers import UserSerializer

from recipes.models import Recipe
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    ...
