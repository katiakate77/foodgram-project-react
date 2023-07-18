from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer

from recipes.models import Recipe
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        serializer_class=UserSerializer,
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    ...
