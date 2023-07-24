from django.db.models import Count
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    UserSerializer, UserCreateSerializer, ResetPasswordSerializer,
    RecipeSerializer, RecipeCreateUpdateSerializer,
    TagSerializer, IngredientSerializer, SubscriptionSerializer
    )

from api.mixins import ListCreateRetrieveViewSet
from recipes.models import Recipe, Tag, Ingredient
from users.models import User
from api.permissions import AccessOrReadOnly


class UserViewSet(ListCreateRetrieveViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return ResetPasswordSerializer
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(
        detail=False,
        serializer_class=UserSerializer,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=('post',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')
            self.request.user.set_password(new_password)
            self.request.user.save()
            return Response(
                {'status': 'password set'}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

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
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Recipe.objects.all()
    permission_classes = (AccessOrReadOnly,)
    search_fields = ('^ingredients__name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

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
