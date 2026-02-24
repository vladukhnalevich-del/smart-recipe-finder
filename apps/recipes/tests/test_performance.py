from django.test import TestCase
from django.urls import reverse
from apps.recipes.models import Recipe
import time
import json


class RecipePerformanceTest(TestCase):
    def setUp(self):
        recipes = []
        for i in range(100):
            recipes.append(Recipe(
                name=f"Рецепт {i}",
                ingredients=f"Ингредиенты {i}",
                instructions=f"Инструкции {i}",
                cooking_time=30,
                cuisine="russian" if i % 2 == 0 else "italian",
                difficulty="easy" if i % 3 == 0 else "medium" if i % 3 == 1 else "hard"
            ))
        Recipe.objects.bulk_create(recipes)

    def test_api_response_time(self):
        url = reverse('recipes:api_recipes')

        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()

        response_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0)

    def test_database_query_count(self):
        url = reverse('recipes:api_recipes')

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_large_payload(self):
        url = reverse('recipes:api_recipes')

        large_text = "A" * 10000
        new_recipe = {
            'name': large_text[:200],
            'ingredients': [large_text for _ in range(5)],
            'instructions': large_text,
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