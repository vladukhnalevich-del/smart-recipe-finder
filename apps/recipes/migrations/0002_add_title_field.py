from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        # Добавляем поле title
        migrations.AddField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),

        # Копируем данные из name в title
        migrations.RunSQL(
            sql='UPDATE recipes_recipe SET title = name;',
            reverse_sql='UPDATE recipes_recipe SET name = title;',
        ),
    ]