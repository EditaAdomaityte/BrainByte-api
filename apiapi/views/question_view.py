from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'user', 'body','answer')
        depth=1

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request):
        try:
            categories = Question.objects.all()
            serializer = QuestionSerializer(
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
            question = Question.objects.get(pk=pk)
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        '''not working'''
        try:
            question = Question.objects.get(pk=pk)
            question.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

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
            question.user = question.user
            question.body = request.data["body"]
            question.answer = request.data["answer"]
            question.save()
        except question.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)