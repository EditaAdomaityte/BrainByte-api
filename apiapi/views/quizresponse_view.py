from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import QuizAttempt, QuizResponse, Question
from rest_framework.exceptions import NotFound


class QuizResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model=QuizResponse
        fields='__all__'
        depth=1


class QuizResponseViewSet(ViewSet):

    def list(self, request):
        try:
            # Check if quizattempt_id is provided in query params
            quizattempt_id = request.query_params.get('quizattempt_id')
            
            if quizattempt_id:
                # Filter responses by quizattempt_id
                quizresponses = QuizResponse.objects.filter(quizattempt_id=quizattempt_id)
                if not quizresponses:
                    return Response({"message": f"No quiz responses found for quizattempt_id={quizattempt_id}"}, 
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                # If no quizattempt_id is provided, return all responses
                quizresponses = QuizResponse.objects.all()
                
            serializer = QuizResponseSerializer(
                quizresponses, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """

        try:

            question_id = request.data.get('question')
            question = Question.objects.get(pk=question_id)

            quizattempt_id = request.data.get('quizattempt')
            quizattempt = QuizAttempt.objects.get(pk=quizattempt_id)

            user_answer=request.data.get('user_answer')
            is_correct = question.answer == bool(user_answer)

            quizresponse = QuizResponse()
            quizresponse.question=question
            quizresponse.user_answer=bool(user_answer)
            quizresponse.quizattempt=quizattempt
            quizresponse.is_correct=is_correct
            quizresponse.save()
            
            serializer = QuizResponseSerializer(quizresponse, context={'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Question.DoesNotExist:
            return Response({"reason": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        except QuizAttempt.DoesNotExist:
            return Response({"reason": "QuizAttempt not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        