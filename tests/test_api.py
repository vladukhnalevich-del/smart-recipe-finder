
from django.test import TestCase
from django.urls import reverse

class RecipeAPITestCase(TestCase):
    def test_get_recipes(self):
        response = self.client.get(reverse('recipes:api_recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_create_recipe(self):
        data = {
            'name': 'Тестовый рецепт',
            'ingredients': ['тест1', 'тест2'],
            'instructions': 'Тестовые инструкции',
            'cooking_time': 30
        }
        response = self.client.post(
            reverse('recipes:api_recipes'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
