# Generated by Django 5.1.2 on 2024-11-01 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_alter_keyword_scheduled_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='scheduled_time',
            field=models.DateTimeField(),
        ),
    ]
