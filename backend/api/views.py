from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    UserSerializer, TagSerializer,
    IngredientSerializer, RecipeIngredientSerializer
    )

from recipes.models import Recipe, Tag, Ingredient
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

    @action(
        detail=False,
        methods=('post',),
        serializer_class=...,
    )
    def set_password(self, request):
        ...

    @action(
        detail=False,
        serializer_class=...,
    )
    def subscriptions(self, request):
        ...

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=...,
    )
    def subscribe(self, request):
        ...


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Recipe.objects.all()

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=...,
    )
    def favorite(self, request):
        ...

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=...,
    )
    def shopping_cart(self, request):
        ...

    @action(
        detail=False,
        serializer_class=...,
    )
    def download_shopping_cart(self, request):
        ...
