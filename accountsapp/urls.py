from django.urls import path

from accountsapp.views import CreateUserView, VerifyEmail

urlpatterns =[
    path('register/', CreateUserView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]