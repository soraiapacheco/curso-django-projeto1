# Generated by Django 4.1.5 on 2023-04-24 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_is_publisched_recipe_is_published'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='preparation_step_is_html',
            new_name='preparation_steps_is_html',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.category'),
        ),
    ]