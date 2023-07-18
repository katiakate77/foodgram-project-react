from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

app_name = 'api'
urlpatterns = [
    path('', include(router_v1.urls)),
]
