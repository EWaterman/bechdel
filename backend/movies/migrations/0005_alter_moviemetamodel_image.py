# Generated by Django 3.2.13 on 2022-07-23 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_moviemetamodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviemetamodel',
            name='image',
            field=models.ImageField(default='posters/default.jpg', upload_to='posters/'),
        ),
    ]
