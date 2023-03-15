# Generated by Django 2.2.16 on 2023-03-15 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20230315_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингредиенты', related_name='ingredient', to='api.Ingredient', verbose_name='Список ингредиентов'),
        ),
    ]
