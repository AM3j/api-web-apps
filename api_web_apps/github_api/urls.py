from django.urls import path
from . import views

urlpatterns =[
    # Paths for our app
    path('', views.Github_View.as_view(), name='github')
]