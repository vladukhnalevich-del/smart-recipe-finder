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
        data = [
            {
                "id": r.id,
                "title": r.title,
                "ingredients": r.ingredients,
                "instructions": r.instructions,
                "cooking_time": r.cooking_time,
                #"created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in recipes
        ]
        response = JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)


            title = data.get('title') or data.get('name')
            if not title:
                return JsonResponse({"error": "Название рецепта обязательно"}, status=400)


            ingredients = data.get('ingredients')
            if not ingredients:
                return JsonResponse({"error": "Ингредиенты обязательны"}, status=400)


            if isinstance(ingredients, list):
                ingredients = '\n'.join(ingredients)


            recipe = Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=data.get('instructions', ''),
                cooking_time=data.get('cooking_time', 30)
            )

            response_data = {
                "id": recipe.id,
                "title": recipe.title,
                "ingredients": recipe.ingredients,
                "instructions": recipe.instructions,
                "cooking_time": recipe.cooking_time,
                #"created_at": recipe.created_at.isoformat() if recipe.created_at else None
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
            data = {
                "id": recipe.id,
                "title": recipe.title,
                "ingredients": recipe.ingredients,
                "instructions": recipe.instructions,
                "cooking_time": recipe.cooking_time,
                #"created_at": recipe.created_at.isoformat() if recipe.created_at else None,
                #"updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None
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