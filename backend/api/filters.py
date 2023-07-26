# from django_filters import rest_framework as django_filters
from rest_framework.filters import SearchFilter

# from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'


# class RecipeFilter(django_filters.FilterSet):
#     tags = django_filters.ModelMultipleChoiceFilter(
#         field_name='tags__slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all()
#     )
