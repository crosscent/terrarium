from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView

from terrarium.web.api.serializers import UserSerializer

class IsStaffOrTargetUser(permissions.BasePermission):
    """
    Defines permission for listing all users, and viewing user detail
    """
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all
        # records
        return request.user.is_staff or obj == request.user

class QuietBasicAuthentication(BasicAuthentication):
    """
    Removes the dialogue box returned if the wrong credentials were provided
    """
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm

class UserView(viewsets.ModelViewSet):
    """
    Responsible for displaying user detail
    """
    model = User
    serializer_class = UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST' else
                IsStaffOrTargetUser()),

    @list_route(methods=['post'], authentication_classes=(QuietBasicAuthentication, ))
    def auth(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)

