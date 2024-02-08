from django.urls import path

from accountsapp.views import CreateUserView, VerifyEmail, UserLoginView, UserDetailView

urlpatterns =[
    path('register/', CreateUserView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
]