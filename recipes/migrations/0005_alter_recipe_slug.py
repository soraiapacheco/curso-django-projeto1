# Generated by Django 4.2 on 2023-05-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_rename_preparation_step_is_html_recipe_preparation_steps_is_html_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
