# from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

# from recipes.models import Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


# class RecipeFilter(filters.FilterSet):
#     tags = filters.ModelMultipleChoiceFilter(
#         field_name='tags__slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all()
#     )
