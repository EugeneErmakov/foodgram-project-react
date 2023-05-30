from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'id',
            'is_subscribed'
        )

