# Generated by Django 5.1.5 on 2025-02-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=bool)),
                ('full_title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
