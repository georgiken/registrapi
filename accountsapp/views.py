import jwt
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, generics, response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser # If used custom user model

from .serializers import UserSerializer, EmailVerificationSerializer
from .utils import Util


class CreateUserView(CreateAPIView):

    model = CustomUser()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

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
        # current_site = get_current_site(request).domain
        # relative_link = reverse('email-verify')
        # absurl = 'http://' + current_site + relative_link + "?token=" + str(tokens)
        email_body = 'Hi ' + user['username'] + ' your verify token:' + str(tokens)
                     # ''' ' Use the link below to verify your email \n' + absurl'''
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': 'Verify your email'}

        Util.send_email(data=data)

        return response.Response(status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView ):
    serializer_class = EmailVerificationSerializer

    # проверка email'a
    # email_param_config = openapi.Parameter(
    #     'email', in_=openapi.IN_QUERY, description='Email to verify', type=openapi.TYPE_STRING)

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):

        token = request.GET.get('token')

        # email = request.GET.get('email')
        # if not email:
        #     return response.Response({'error': 'Email is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({'username': request.user.username}, status=status.HTTP_200_OK)

class Zaglushka(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )