# Generated by Django 5.1.5 on 2025-03-12 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbi_app', '0002_tag_remove_project_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='project',
            name='main_image',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Zdjęcie 1'), (2, 'Zdjęcie 2'), (3, 'Zdjęcie 3'), (4, 'Zdjęcie 4')], help_text='Wybierz numer zdjęcia, które ma być głównym', null=True),
        ),
    ]
