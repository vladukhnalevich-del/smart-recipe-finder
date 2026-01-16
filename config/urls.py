from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

RECIPES_DB = [{"id": 1, "name": "Борщ", "ingredients": ["вода", "бурак", "мясо"]}]


@csrf_exempt
def api_recipes(request):
    if request.method == 'GET':
        return JsonResponse(RECIPES_DB, safe=False, json_dumps_params={'ensure_ascii': False})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not data.get('name'):
                return JsonResponse({"error": "Название рецепта обязательно"}, status=400)

            cooking_time = data.get('cooking_time', 30)
            try:
                cooking_time = float(cooking_time)
                if cooking_time <= 0:
                    return JsonResponse({"error": "Время готовки должно быть положительным числом"}, status=400)
            except:
                return JsonResponse({"error": "Время готовки должно быть числом"}, status=400)

            new_id = max([r['id'] for r in RECIPES_DB], default=0) + 1
            new_recipe = {
                "id": new_id,
                "name": data['name'],
                "ingredients": data.get('ingredients', []),
                "instructions": data.get('instructions', ""),
                "cooking_time": cooking_time
            }

            RECIPES_DB.append(new_recipe)
            return JsonResponse(new_recipe, status=201, json_dumps_params={'ensure_ascii': False})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def api_recipe_detail(request, id):
    try:
        recipe = next((r for r in RECIPES_DB if r['id'] == id), None)
        if not recipe:
            return JsonResponse({"error": "Рецепт не найден"}, status=404)

        if request.method == 'GET':
            return JsonResponse(recipe, json_dumps_params={'ensure_ascii': False})
        elif request.method == 'DELETE':
            RECIPES_DB[:] = [r for r in RECIPES_DB if r['id'] != id]
            return JsonResponse({"success": True, "message": f"Рецепт {id} удален"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def home_view(request):
    html = '<html><body><h1>Smart Recipe Finder</h1><p>Добро пожаловать!</p><ul><li><a href="/client/">Клиент</a></li><li><a href="/api/recipes/">API</a></li></ul></body></html>'
    return HttpResponse(html)


def client_view(request):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Smart Recipe Finder</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            .container { max-width: 800px; margin: auto; }
            h1 { text-align: center; }
            .buttons { margin: 20px 0; text-align: center; }
            .btn { padding: 10px 20px; margin: 5px; border: none; cursor: pointer; color: white; border-radius: 5px; }
            .btn-get { background: #4CAF50; }
            .btn-post { background: #2196F3; }
            .btn-delete { background: #f44336; }
            input, textarea { width: 100%; padding: 8px; margin: 5px 0; border: 1px solid #ddd; box-sizing: border-box; }
            .result { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Smart Recipe Finder</h1>
            <div class="buttons">
                <button class="btn btn-get" onclick="getRecipes()">Получить рецепты</button>
                <button class="btn btn-post" onclick="postRecipe()">Создать рецепт</button>
                <button class="btn btn-delete" onclick="deleteRecipe()">Удалить рецепт</button>
            </div>
            <div><label>ID рецепта (для удаления):</label><input type="text" id="recipeId" placeholder="Введите ID"></div>
            <div><label>Название рецепта:</label><input type="text" id="name" placeholder="Название рецепта"></div>
            <div><label>Ингредиенты (через запятую):</label><textarea id="ingredients" placeholder="ингредиент1, ингредиент2" rows="3" style="resize: none;"></textarea></div>
            <div><label>Инструкции:</label><textarea id="instructions" placeholder="Инструкции" rows="4" style="resize: none;"></textarea></div>
            <div><label>Время готовки (минуты):</label><input type="number" id="cooking_time" value="30" min="1" max="1000"></div>
            <div class="result" id="result">Нажмите кнопку для работы с API</div>
        </div>
        <script>
            const API_URL = '/api/recipes/';
            async function getRecipes() {
                try {
                    const response = await fetch(API_URL);
                    const data = await response.json();
                    document.getElementById('result').innerHTML = 'GET успешен:\\n' + JSON.stringify(data, null, 2);
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Ошибка GET: ' + error;
                }
            }
            async function postRecipe() {
                const name = document.getElementById('name').value.trim();
                if (!name) { alert('Введите название рецепта'); return; }
                const ingredients = document.getElementById('ingredients').value.split(',').map(i => i.trim()).filter(i => i.length > 0);
                let cooking_time = document.getElementById('cooking_time').value.trim();
                if (cooking_time === '') cooking_time = 30;
                cooking_time = parseFloat(cooking_time);
                if (isNaN(cooking_time) || cooking_time <= 0) { alert('Время готовки должно быть положительным числом'); return; }
                const recipeData = { name: name, ingredients: ingredients, instructions: document.getElementById('instructions').value.trim(), cooking_time: cooking_time };
                try {
                    const response = await fetch(API_URL, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(recipeData) });
                    const data = await response.json();
                    if (response.ok) {
                        document.getElementById('result').innerHTML = 'POST успешен:\\n' + JSON.stringify(data, null, 2);
                        document.getElementById('name').value = '';
                        document.getElementById('ingredients').value = '';
                        document.getElementById('instructions').value = '';
                    } else {
                        document.getElementById('result').innerHTML = 'Ошибка: ' + JSON.stringify(data);
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Ошибка POST: ' + error;
                }
            }
            async function deleteRecipe() {
                const id = document.getElementById('recipeId').value.trim();
                if (!id) { alert('Введите ID рецепта для удаления'); return; }
                if (!confirm('Удалить рецепт ' + id + '?')) return;
                try {
                    const response = await fetch(API_URL + id + '/', { method: 'DELETE' });
                    const data = await response.json();
                    if (response.ok) {
                        document.getElementById('result').innerHTML = 'DELETE успешен:\\n' + JSON.stringify(data, null, 2);
                        document.getElementById('recipeId').value = '';
                    } else {
                        document.getElementById('result').innerHTML = 'Ошибка: ' + JSON.stringify(data);
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Ошибка DELETE: ' + error;
                }
            }
            window.onload = getRecipes;
        </script>
    </body>
    </html>
    '''
    return HttpResponse(html)


urlpatterns = [
    path('', home_view),
    path('api/recipes/', api_recipes),
    path('api/recipes/<int:id>/', api_recipe_detail),
    path('client/', client_view),
]