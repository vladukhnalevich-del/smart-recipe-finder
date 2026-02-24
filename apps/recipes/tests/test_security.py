from django.test import TestCase
from django.urls import reverse
from apps.recipes.models import Recipe
import json


class RecipeSecurityTest(TestCase):
    def test_sql_injection(self):
        url = reverse('recipes:api_recipes')

        malicious_input = "'; DROP TABLE recipes_recipe; --"
        new_recipe = {
            'name': malicious_input,
            'ingredients': [malicious_input],
            'instructions': malicious_input,
            'cooking_time': 30,
            'cuisine': malicious_input,
            'difficulty': 'easy'
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        saved_recipe = Recipe.objects.get(name=malicious_input)
        self.assertEqual(saved_recipe.name, malicious_input)

    def test_xss_attack(self):
        url = reverse('recipes:api_recipes')

        xss_payload = '<script>alert("XSS")</script>'
        new_recipe = {
            'name': xss_payload,
            'ingredients': [xss_payload],
            'instructions': xss_payload,
            'cooking_time': 30,
            'cuisine': 'russian',
            'difficulty': 'easy'
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        get_response = self.client.get(url)
        data = get_response.json()

        latest_recipe = data[-1]
        self.assertIn('<script>', latest_recipe['name'])
        self.assertIn('alert', latest_recipe['name'])

    def test_json_injection(self):
        url = reverse('recipes:api_recipes')

        malicious_json = '{"name": "test", "ingredients": ["ing1"], "cooking_time": 30}'

        response = self.client.post(
            url,
            data=malicious_json,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

    def test_very_deep_json(self):
        url = reverse('recipes:api_recipes')

        deep_object = {}
        current = deep_object
        for i in range(50):
            current['level' + str(i)] = {}
            current = current['level' + str(i)]

        response = self.client.post(
            url,
            data=json.dumps(deep_object),
            content_type='application/json'
        )

        self.assertIn(response.status_code, [400, 500])