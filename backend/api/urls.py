from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet, UserViewSet


router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet, basename='recipes')

app_name = 'api'
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
