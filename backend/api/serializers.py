from rest_framework import serializers

from recipes.models import Ingredient, Tag
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        model = User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
