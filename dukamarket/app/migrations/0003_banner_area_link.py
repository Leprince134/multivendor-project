# Generated by Django 4.0.6 on 2022-08-03 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_banner_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner_area',
            name='Link',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
