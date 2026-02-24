from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('cooking_time', models.IntegerField()),
                ('cuisine', models.CharField(choices=[('russian', 'Русская кухня'), ('belarusian', 'Белорусская кухня'), ('ukrainian', 'Украинская кухня'), ('italian', 'Итальянская кухня'), ('french', 'Французская кухня'), ('chinese', 'Китайская кухня'), ('japanese', 'Японская кухня'), ('mexican', 'Мексиканская кухня'), ('georgian', 'Грузинская кухня'), ('american', 'Американская кухня'), ('other', 'Другая кухня')], default='russian', max_length=20)),
                ('difficulty', models.CharField(choices=[('easy', 'Легко'), ('medium', 'Средняя'), ('hard', 'Сложно')], default='medium', max_length=10)),
            ],
        ),
    ]
