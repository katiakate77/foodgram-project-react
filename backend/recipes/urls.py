from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'
urlpatterns = [
    path('', include(router.urls)),
]
