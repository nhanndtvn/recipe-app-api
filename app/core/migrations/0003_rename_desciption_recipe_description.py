# Generated by Django 5.0.1 on 2024-01-17 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='desciption',
            new_name='description',
        ),
    ]
