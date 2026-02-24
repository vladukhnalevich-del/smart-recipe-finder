from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.recipes.models import Recipe


class RecipeValidationTest(TestCase):
    def test_cuisine_invalid_value(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=30,
            cuisine="несуществующая_кухня",
            difficulty="easy"
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_difficulty_invalid_value(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=30,
            cuisine="russian",
            difficulty="очень_сложно"
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_cuisine_valid_values(self):
        valid_cuisines = ['russian', 'italian', 'french', 'chinese', 'japanese']
        for cuisine in valid_cuisines:
            recipe = Recipe(
                name="Тест",
                ingredients="ингредиенты",
                instructions="инструкции",
                cooking_time=30,
                cuisine=cuisine,
                difficulty="easy"
            )
            try:
                recipe.full_clean()
            except ValidationError:
                self.fail(f"Значение {cuisine} должно быть допустимым")

    def test_difficulty_valid_values(self):
        valid_difficulties = ['easy', 'medium', 'hard']
        for difficulty in valid_difficulties:
            recipe = Recipe(
                name="Тест",
                ingredients="ингредиенты",
                instructions="инструкции",
                cooking_time=30,
                cuisine="russian",
                difficulty=difficulty
            )
            try:
                recipe.full_clean()
            except ValidationError:
                self.fail(f"Значение {difficulty} должно быть допустимым")

    def test_cooking_time_negative(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=-10,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.cooking_time, -10)

    def test_cooking_time_zero(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=0,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.cooking_time, 0)

    def test_cooking_time_large(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=999999,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.cooking_time, 999999)

    def test_empty_name(self):
        recipe = Recipe(
            name="",
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.name, "")

    def test_empty_ingredients(self):
        recipe = Recipe(
            name="Тест",
            ingredients="",
            instructions="инструкции",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.ingredients, "")

    def test_empty_instructions(self):
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions="",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.instructions, "")

    def test_very_long_name(self):
        long_name = "А" * 1000
        recipe = Recipe(
            name=long_name,
            ingredients="ингредиенты",
            instructions="инструкции",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(len(saved_recipe.name), 1000)

    def test_very_long_ingredients(self):
        long_ingredients = "Ингредиент\n" * 100
        recipe = Recipe(
            name="Тест",
            ingredients=long_ingredients,
            instructions="инструкции",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(len(saved_recipe.ingredients.split('\n')), 100)

    def test_very_long_instructions(self):
        long_instructions = "Шаг 1\n" * 100
        recipe = Recipe(
            name="Тест",
            ingredients="ингредиенты",
            instructions=long_instructions,
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(len(saved_recipe.instructions.split('\n')), 100)

    def test_special_characters(self):
        recipe = Recipe(
            name="Рецепт №1 с @#$% символами",
            ingredients="ингредиент & специи *",
            instructions="шаг 1: сделать % | шаг 2: проверить",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.name, "Рецепт №1 с @#$% символами")
        self.assertIn("@", saved_recipe.name)
        self.assertIn("#", saved_recipe.name)
        self.assertIn("$", saved_recipe.name)

    def test_spaces_only(self):
        recipe = Recipe(
            name="   ",
            ingredients="   ",
            instructions="   ",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.name, "   ")
        self.assertEqual(saved_recipe.ingredients, "   ")
        self.assertEqual(saved_recipe.instructions, "   ")

    def test_newlines_only(self):
        recipe = Recipe(
            name="\n\n\n",
            ingredients="\n\n\n",
            instructions="\n\n\n",
            cooking_time=30,
            cuisine="russian",
            difficulty="easy"
        )
        recipe.save()
        saved_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(saved_recipe.name, "\n\n\n")
        self.assertEqual(saved_recipe.ingredients, "\n\n\n")
        self.assertEqual(saved_recipe.instructions, "\n\n\n")