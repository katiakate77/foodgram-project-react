# from django.db.models import Count
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import IngredientFilter
from api.mixins import ListCreateRetrieveViewSet
from api.permissions import AccessOrReadOnly
from api.serializers import (
    IngredientSerializer, RecipeCreateUpdateSerializer, RecipeSerializer,
    RecipeShortSerializer, ResetPasswordSerializer,
    SubscriptionSerializer, TagSerializer,
    UserCreateSerializer, UserSerializer
)
from recipes.models import (
    FavoriteRecipe, Ingredient, Recipe,
    RecipeIngredient, ShoppingCart, Tag
)
from users.models import Follow, User


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
        # queryset = (User.objects.filter(following__user=request.user)
        #             .annotate(recipes_count=Count('recipes'))
        #             )
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author, data=request.data, context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                Follow.objects.create(user=user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'error': 'Вы не были подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Recipe.objects.all()
    permission_classes = (AccessOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_or_shopping_cart(self, request, model, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = RecipeShortSerializer(
                recipe, data=request.data, context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                model.objects.create(user=user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            get_object_or_404(model, user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return self.favorite_or_shopping_cart(request, FavoriteRecipe, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        return self.favorite_or_shopping_cart(request, ShoppingCart, pk)

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        recipes = request.user.shoppingcart.all().values('recipe__id')
        ingredients = RecipeIngredient.objects.filter(recipe__in=recipes)

        if not ingredients:
            return Response(
                {'errors': 'Список покупок пустой'},
                status=status.HTTP_204_NO_CONTENT
            )
        total_ingredients = ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(amount=Sum('amount'))
        return make_file(
            ('Наименование', 'Единица измерения', 'Количество'),
            total_ingredients, 'shopping_cart.txt', status.HTTP_200_OK)


def make_file(header, data, filename, http_status):
    product_list = []
    for ingredient in data:
        product_list.append(
            '{name} ({unit}) - {amount}'.format(
                name=ingredient['ingredient__name'],
                unit=ingredient['ingredient__measurement_unit'],
                amount=ingredient['amount']
            )
        )
    response = HttpResponse(
        content='\n'.join(product_list),
        content_type='text/plain',
        status=http_status
    )
    response['Content-Disposition'] = (
        f'attachment; filename={filename}')
    return response
