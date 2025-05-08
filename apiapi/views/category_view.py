from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import Category
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'url')
        depth=1

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(
            categories, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)