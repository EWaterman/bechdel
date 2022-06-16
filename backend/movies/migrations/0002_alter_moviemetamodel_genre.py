# Generated by Django 3.2.13 on 2022-06-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviemetamodel',
            name='genre',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Action'), (1, 'Horror'), (2, 'Comedy'), (3, 'Adventure'), (4, 'Drama'), (5, 'Thriller/Suspense'), (6, 'Musical'), (7, 'Romantic Comedy'), (8, 'Western'), (9, 'Black Comedy')], db_index=True),
        ),
    ]
