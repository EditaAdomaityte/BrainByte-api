from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import QuizAttempt, Category
from rest_framework.permissions import IsAuthenticated


class QuizAttemptSerializer(serializers.ModelSerializer):

    class Meta:
        model=QuizAttempt
        fields=('id', 'user','category','question_count','created_date','result')
        depth=1


class QuizAttemptViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user=request.user
            myquizattempts=QuizAttempt.objects.filter(user=user)
            serializer=QuizAttemptSerializer(
                myquizattempts, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            quizattempt = QuizAttempt.objects.get(pk=pk)
            serializer = QuizAttemptSerializer(quizattempt, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """

        try:

            category_id = request.data.get('category')
            category = Category.objects.get(pk=category_id)

            quizattempt = QuizAttempt()
            quizattempt.user=request.user
            quizattempt.category=category
            quizattempt.question_count=request.data.get('question_count')
            quizattempt.save()

            serializer = QuizAttemptSerializer(quizattempt, context={'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)