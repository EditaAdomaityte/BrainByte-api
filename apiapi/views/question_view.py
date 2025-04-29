from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'user', 'body','answer')
        depth=1

class QuestionViewSet(ViewSet):

    queryset = Question.objects.all()
   

    def list(self, request):
        try:
            questions = Question.objects.all()
            serializer = QuestionSerializer(
            questions, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        '''not working'''
        try:
            question = Question.objects.get(pk=pk)
            if question.user.id!=request.user.id:
                return Response('You are not the user who wrote this question',status=status.HTTP_403_FORBIDDEN)
            question.delete()
            return Response('Question was deleted successfully.', status=status.HTTP_204_NO_CONTENT)

        except Question.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
    def update(self, request, pk=None):
        """Handle PUT requests NOT TESTED

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            question = Question.objects.get(pk=pk)
            if question.user.id!=request.user.id:
                return Response('You are not the user who wrote this question',status=status.HTTP_403_FORBIDDEN)
            question.user = question.user
            question.body = request.data["body"]
            question.answer = request.data["answer"]
            question.save()
        except question.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        question = Question()
        question.user=request.user
        question.body=request.data.get('body')
        question.answer=request.data.get('answer')

        try:
            question.save()
            serializer = QuestionSerializer(question, context={'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)