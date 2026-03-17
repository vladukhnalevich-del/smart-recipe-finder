from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET', 'POST'])
def api_recipes(request):

    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные невалидны кидает ошибку
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def api_recipe_detail(request, id):

    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response({"error": "Рецепт не найден"},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response({"success": True, "message": f"Рецепт {id} удален"},
                        status=status.HTTP_200_OK)

def home_view(request):
    #Главная страница
    return render(request, 'recipes/home.html')


def client_view(request):
    #Клиентский интерфейс
    context = {
        'cuisine_choices': Recipe.CUISINE_CHOICES,
        'difficulty_choices': Recipe.DIFFICULTY_CHOICES,
    }
    return render(request, 'recipes/client.html', context)