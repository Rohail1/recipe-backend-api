""""
    User API Views
"""

from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserSerializer(generics.CreateAPIView):
    """ Create new user in the system """
    serializer_class = UserSerializer