from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

from accountsapp.models import CustomUser

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", 'email', "password", )


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = CustomUser
        fields = ['token']