from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apiapi.models import QuestionCategory, Question, Category


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ('id', 'question', 'category')
        depth = 1
        

class QuestionCategoryViewSet(ViewSet):

    def list(self, request):
        try:
            question_id = request.query_params.get('question_id')
            
            if question_id:
                # Filter responses by question_id
                questioncategories = QuestionCategory.objects.filter(question_id=question_id)
                if not questioncategories:
                    return Response({"message": f"No categories found for question_id={question_id}"}, 
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                # If no question_id is provided, return all responses
                 questioncategories = QuestionCategory.objects.all()
                
            serializer = QuestionCategorySerializer(
                questioncategories, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        """Handle POST operations to create a question-category relationship

        Returns:
            Response -- JSON serialized QuestionCategory instance
        """
        try:
            question_id = request.data.get('question_id')
            category_id = request.data.get('category_id')
            
            question = Question.objects.get(pk=question_id)
            category = Category.objects.get(pk=category_id)
            
            question_category = QuestionCategory()
            question_category.question = question
            question_category.category = category
            question_category.save()
            
            serializer = QuestionCategorySerializer(question_category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Question.DoesNotExist:
            return Response({"reason": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"reason": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)