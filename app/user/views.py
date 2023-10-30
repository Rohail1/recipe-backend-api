""""
    User API Views
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """ Create new user in the system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a user token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileView(generics.RetrieveUpdateAPIView):
    """ Retrieve and Update view for Profile"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve User Item """
        return self.request.user
