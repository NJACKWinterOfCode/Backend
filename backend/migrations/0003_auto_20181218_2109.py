# Generated by Django 2.1 on 2018-12-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_charts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charts',
            name='table_name',
            field=models.CharField(max_length=100),
        ),
    ]