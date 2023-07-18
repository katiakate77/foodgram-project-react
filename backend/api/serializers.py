from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )
        model = User
