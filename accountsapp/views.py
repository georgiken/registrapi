from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import permissions, generics, response, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser # If used custom user model

from .serializers import UserSerializer
from .utils import Util


class CreateUserView(CreateAPIView):

    model = CustomUser()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        user_email = CustomUser.objects.get(email=user['email'])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + "?token=" + str(tokens)
        email_body = 'Hi ' + user['username'] + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': 'Verify your email'}

        Util.send_email(data=data)

        return response.Response({'user_data': user, 'access_token' : str(tokens)}, status=status.HTTP_201_CREATED)



class Zaglushka(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )