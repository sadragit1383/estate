# Generated by Django 4.2 on 2025-06-08 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={},
        ),
        migrations.AlterModelOptions(
            name='advertisementtype',
            options={},
        ),
        migrations.AlterModelOptions(
            name='propertytype',
            options={},
        ),
        migrations.AlterModelOptions(
            name='typepremium',
            options={},
        ),
        migrations.AddField(
            model_name='advertisement',
            name='features',
            field=models.ManyToManyField(to='estate.feature'),
        ),
    ]
