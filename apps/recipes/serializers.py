from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name', read_only=True)


    ingredients = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    ingredients_display = serializers.CharField(
        source='ingredients',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'title', 'ingredients', 'ingredients_display',
                  'instructions', 'cooking_time', 'cuisine', 'difficulty']
        read_only_fields = ['id']

    def create(self, validated_data):

        ingredients_list = validated_data.pop('ingredients', [])

        ingredients_str = '\n'.join(ingredients_list) if ingredients_list else ''

        recipe = Recipe.objects.create(
            ingredients=ingredients_str,
            **validated_data
        )
        return recipe

    def update(self, instance, validated_data):

        ingredients_list = validated_data.pop('ingredients', None)
        if ingredients_list is not None:
            instance.ingredients = '\n'.join(ingredients_list)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if instance.ingredients:
            data['ingredients_list'] = instance.ingredients.split('\n')
        else:
            data['ingredients_list'] = []
        return data