from rest_framework import viewsets

from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    ...
