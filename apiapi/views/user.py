from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializers
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'username', 'password', 'first_name', 'last_name', 'email','is_staff', 'is_active', 'date_joined')


class Users(ViewSet):
    """Users for BrainByte
    Purpose: Allow a user to communicate with the BrainByte database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
"""
    def get_permissions(self):
        if self.action == 'partial_update':
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Purpose: Allow a user to communicate with the BrainByte database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)
    

    def partial_update(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to edit users."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(pk=pk)
            for attr, value in request.data.items():
                setattr(user, attr, value)
            user.save()
            return Response({"message": "User updated."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)