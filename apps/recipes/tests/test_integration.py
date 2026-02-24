from django.test import TestCase
from django.urls import reverse
import json
from apps.recipes.models import Recipe


class RecipeIntegrationTest(TestCase):


    def test_full_recipe_workflow(self):



        url = reverse('recipes:api_recipes')
        new_recipe = {
            'name': 'Интеграционный тест',
            'ingredients': ['инг1', 'инг2'],
            'instructions': 'шаг1\nшаг2',
            'cooking_time': 45,
            'cuisine': 'georgian',
            'difficulty': 'medium'
        }

        create_response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(create_response.status_code, 201)
        recipe_id = create_response.json()['id']


        get_url = reverse('recipes:api_recipe_detail', args=[recipe_id])
        get_response = self.client.get(get_url)

        self.assertEqual(get_response.status_code, 200)
        recipe_data = get_response.json()
        self.assertEqual(recipe_data['cuisine'], 'georgian')


        delete_response = self.client.delete(get_url)
        self.assertEqual(delete_response.status_code, 200)