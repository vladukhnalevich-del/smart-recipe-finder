from django.test import TestCase
from apps.recipes.models import Recipe


class RecipeModelTest(TestCase):


    def setUp(self):

        self.recipe = Recipe.objects.create(
            name="Тестовый рецепт",
            ingredients="Ингредиент 1\nИнгредиент 2\nИнгредиент 3",
            instructions="Шаг 1\nШаг 2\nШаг 3",
            cooking_time=45,
            cuisine="italian",
            difficulty="medium"
        )

    def test_recipe_creation(self):

        self.assertEqual(self.recipe.name, "Тестовый рецепт")
        self.assertEqual(self.recipe.ingredients, "Ингредиент 1\nИнгредиент 2\nИнгредиент 3")
        self.assertEqual(self.recipe.instructions, "Шаг 1\nШаг 2\nШаг 3")
        self.assertEqual(self.recipe.cooking_time, 45)
        self.assertEqual(self.recipe.cuisine, "italian")
        self.assertEqual(self.recipe.difficulty, "medium")

    def test_recipe_str_method(self):

        self.assertEqual(str(self.recipe), "Тестовый рецепт")

    def test_default_values(self):

        recipe = Recipe.objects.create(
            name="Рецепт с дефолтными значениями",
            ingredients="Ингредиенты",
            instructions="Инструкции",
            cooking_time=30
        )
        self.assertEqual(recipe.cuisine, "russian")
        self.assertEqual(recipe.difficulty, "medium")


