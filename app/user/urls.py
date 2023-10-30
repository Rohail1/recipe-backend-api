"""
    Urls Mapping for user API
"""

from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserSerializer.as_view(), name="create")
]