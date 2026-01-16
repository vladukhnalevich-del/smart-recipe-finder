
from django.http import HttpResponse
import json



def list_recipes(request):

    recipes = [
        {"id": 1, "name": "Pasta Carbonara", "ingredients": ["pasta", "eggs", "bacon"]},
        {"id": 2, "name": "Caesar Salad", "ingredients": ["lettuce", "croutons", "cheese"]}
    ]
    return HttpResponse(json.dumps(recipes), content_type='application/json')


def recipe_detail(request, id):

    recipe = {"id": id, "name": f"Recipe {id}", "ingredients": []}
    return HttpResponse(json.dumps(recipe), content_type='application/json')



