from django.test import TestCase
from django.urls import reverse
import json
from apps.recipes.models import Recipe


class RecipeAPITestCase(TestCase):

    def setUp(self):
        self.recipe1 = Recipe.objects.create(
            name="Борщ",
            ingredients="Свекла\nКапуста\nМорковь",
            instructions="Сварить",
            cooking_time=90,
            cuisine="russian",
            difficulty="medium"
        )

        self.recipe2 = Recipe.objects.create(
            name="Паста",
            ingredients="Спагетти\nСоус",
            instructions="Сварить",
            cooking_time=30,
            cuisine="italian",
            difficulty="easy"
        )

    def test_get_all_recipes(self):
        url = reverse('recipes:api_recipes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

        self.assertIn('cuisine', data[0])
        self.assertIn('difficulty', data[0])


    def test_create_recipe(self):
        url = reverse('recipes:api_recipes')
        new_recipe = {
            'name': 'Новый рецепт',
            'ingredients': ['инг1', 'инг2'],
            'instructions': 'инструкция',
            'cooking_time': 60,
            'cuisine': 'french',
            'difficulty': 'hard'
        }

        response = self.client.post(
            url,
            data=json.dumps(new_recipe),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['name'], 'Новый рецепт')
        self.assertEqual(data['cuisine'], 'french')
        self.assertEqual(data['difficulty'], 'hard')

