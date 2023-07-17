from django.contrib import admin

from recipes.models import (
    Ingredient, Tag, Recipe, RecipeIngredient, FavoriteRecipe, ShoppingCart)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'cooking_time'
    )
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')


admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)
