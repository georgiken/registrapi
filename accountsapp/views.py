from django.http import HttpResponse
from rest_framework import permissions, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import CustomUser # If used custom user model

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = CustomUser()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class Zaglushka(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )