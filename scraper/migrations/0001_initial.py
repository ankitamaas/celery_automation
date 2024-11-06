# Generated by Django 5.1.2 on 2024-10-28 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('position', models.IntegerField()),
                ('page_number', models.IntegerField()),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.keyword')),
            ],
        ),
    ]
