from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import Question, Category, QuestionCategory
from rest_framework.permissions import IsAuthenticated

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class QuestionSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'user', 'body','answer','approved', 'categories')
        depth=1

    def get_categories(self, obj):
        from apiapi.models import QuestionCategory
        question_categories = QuestionCategory.objects.filter(question=obj)
        return CategorySerializer([qc.category for qc in question_categories], many=True).data

class QuestionViewSet(ViewSet):
    from rest_framework.permissions import IsAuthenticated

    queryset = Question.objects.all()

    def list(self, request):
        try:
            category_id = request.query_params.get('category_id')
            user_only = request.query_params.get('mine') == 'true'
            is_staff = request.user.is_staff

            if category_id:
                # Filter by category AND approval
                question_ids = QuestionCategory.objects.filter(
                    category_id=category_id
                ).values_list('question_id', flat=True).distinct()

                questions = Question.objects.filter(id__in=question_ids, approved=True)

            elif user_only:
                # Only get current user's questions
                questions = Question.objects.filter(user=request.user)

            elif is_staff:
                # Admin sees all questions
                questions = Question.objects.all()

            else:
                # Non-staff user sees only their own questions by default
                questions = Question.objects.filter(user=request.user)

            if not questions.exists():
                return Response({"message": "No questions found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = QuestionSerializer(questions, many=True, context={'request': request})
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
        
    def partial_update(self, request, pk=None):
        try: 
            question=Question.objects.get(pk=pk)
            for attr, value in request.data.items():
                setattr(question, attr, value)
            
            question.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)