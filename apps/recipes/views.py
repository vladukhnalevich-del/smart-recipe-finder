from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Recipe


@csrf_exempt
def api_recipes(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        data = []
        for r in recipes:
            ingredients_list = r.ingredients.split('\n') if r.ingredients else []

            recipe_data = {
                "id": r.id,
                "name": r.name,
                "ingredients": ingredients_list,
                "instructions": r.instructions,
                "cooking_time": r.cooking_time,
                "cuisine": r.cuisine,
                "difficulty": r.difficulty
            }
            data.append(recipe_data)

        response = JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)


            name = data.get('name') or data.get('title')
            if not name:
                return JsonResponse({"error": "Название рецепта обязательно"}, status=400)


            ingredients = data.get('ingredients', '')
            if isinstance(ingredients, list):
                ingredients = '\n'.join(ingredients)

            recipe = Recipe.objects.create(
                name=name,
                ingredients=ingredients,
                instructions=data.get('instructions', ''),
                cooking_time=data.get('cooking_time', 30),

                cuisine=data.get('cuisine', 'russian'),
                difficulty=data.get('difficulty', 'medium')
            )


            ingredients_list = recipe.ingredients.split('\n') if recipe.ingredients else []

            response_data = {
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": ingredients_list,
                "instructions": recipe.instructions,
                "cooking_time": recipe.cooking_time,
                "cuisine": recipe.cuisine,
                "difficulty": recipe.difficulty
            }
            return JsonResponse(response_data, status=201, json_dumps_params={'ensure_ascii': False})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def api_recipe_detail(request, id):
    try:
        recipe = Recipe.objects.get(id=id)

        if request.method == 'GET':
            ingredients_list = recipe.ingredients.split('\n') if recipe.ingredients else []

            data = {
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": ingredients_list,
                "instructions": recipe.instructions,
                "cooking_time": recipe.cooking_time,
                "cuisine": recipe.cuisine,
                "difficulty": recipe.difficulty
            }
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

        elif request.method == 'DELETE':
            recipe.delete()
            return JsonResponse({"success": True, "message": f"Рецепт {id} удален"})

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Рецепт не найден"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def home_view(request):
    return render(request, 'recipes/home.html')


def client_view(request):
    return render(request, 'recipes/client.html')