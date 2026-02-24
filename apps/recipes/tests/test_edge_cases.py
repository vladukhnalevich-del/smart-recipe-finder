from django.test import TestCase
from django.urls import reverse
import json
from apps.recipes.models import Recipe


class RecipeEdgeCasesTest(TestCase):
    def test_empty_database(self):
        Recipe.objects.all().delete()
        url = reverse('recipes:api_recipes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_max_records(self):
        for i in range(100):
            Recipe.objects.create(
                name=f"Рецепт {i}",
                ingredients=f"Ингредиенты {i}",
                instructions=f"Инструкции {i}",
                cooking_time=30,
                cuisine="russian" if i % 2 == 0 else "italian",
                difficulty="easy" if i % 3 == 0 else "medium" if i % 3 == 1 else "hard"
            )

        url = reverse('recipes:api_recipes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 100)

    def test_special_characters_in_api(self):
        url = reverse('recipes:api_recipes')
        new_recipe = {
            'name': 'Рецепт с кавычками "двойными" и /слешами\\',
            'ingredients': ['ингредиент 1', 'ингредиент "с кавычками"', 'ингредиент /со слешем\\'],
            'instructions': 'Шаг 1: "делай так"\nШаг 2: делай / так \\',
            'cooking_time': 30,
            'cuisine': 'russian',
            'difficulty': 'medium'
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('кавычками', data['name'])
        self.assertIn('слешами', data['name'])

    def test_malformed_json(self):
        url = reverse('recipes:api_recipes')
        response = self.client.post(
            url,
            data='{"name": "тест", отсутствует кавычка',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_wrong_content_type(self):
        url = reverse('recipes:api_recipes')
        response = self.client.post(
            url,
            data='name=тест&ingredients=ингредиент',
            content_type='application/x-www-form-urlencoded'
        )
        self.assertIn(response.status_code, [400, 415])

    def test_create_recipe_without_required_fields(self):
        url = reverse('recipes:api_recipes')
        new_recipe = {
            'ingredients': ['ингредиент 1'],
            'instructions': 'инструкция',
            'cooking_time': 30
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_create_recipe_with_empty_ingredients(self):
        url = reverse('recipes:api_recipes')
        new_recipe = {
            'name': 'Тестовый рецепт',
            'ingredients': [],
            'instructions': 'инструкция',
            'cooking_time': 30
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_recipe(self):
        url = reverse('recipes:api_recipe_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_recipe(self):
        url = reverse('recipes:api_recipe_detail', args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_create_recipe_with_long_values(self):
        url = reverse('recipes:api_recipes')
        long_string = "А" * 1000

        new_recipe = {
            'name': long_string[:200],
            'ingredients': [long_string[:500] for _ in range(3)],
            'instructions': long_string * 5,
            'cooking_time': 30,
            'cuisine': 'russian',
            'difficulty': 'medium'
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(len(data['name']), 200)