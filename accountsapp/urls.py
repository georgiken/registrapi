from django.urls import path

from accountsapp.views import CreateUserView

urlpatterns =[
    path('register/', CreateUserView.as_view())
]