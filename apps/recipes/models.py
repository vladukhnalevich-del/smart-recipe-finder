from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()

    CUISINE_CHOICES = [
        ('russian', 'Русская кухня'),
        ('belarusian', 'Белорусская кухня'),
        ('ukrainian', 'Украинская кухня'),
        ('italian', 'Итальянская кухня'),
        ('french', 'Французская кухня'),
        ('chinese', 'Китайская кухня'),
        ('japanese', 'Японская кухня'),
        ('mexican', 'Мексиканская кухня'),
        ('georgian', 'Грузинская кухня'),
        ('american', 'Американская кухня'),
        ('other', 'Другая кухня'),
    ]
    cuisine = models.CharField(
        max_length=20,
        choices=CUISINE_CHOICES,
        default='russian'
    )

    DIFFICULTY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )

    def __str__(self):
        return self.name