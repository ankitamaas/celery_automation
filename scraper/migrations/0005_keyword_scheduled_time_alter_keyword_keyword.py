# Generated by Django 5.1.2 on 2024-10-29 04:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_alter_keyword_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='scheduled_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(max_length=255),
        ),
    ]
