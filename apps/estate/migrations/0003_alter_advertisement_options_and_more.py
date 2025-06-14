# Generated by Django 4.2 on 2025-06-08 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0002_alter_advertisement_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'verbose_name': 'آگهی', 'verbose_name_plural': 'آگهی\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='advertisementtype',
            options={'verbose_name': 'نوع آگهی', 'verbose_name_plural': 'انواع آگهی'},
        ),
        migrations.AlterModelOptions(
            name='propertytype',
            options={'verbose_name': 'نوع ملک', 'verbose_name_plural': 'انواع ملک'},
        ),
        migrations.AlterModelOptions(
            name='typepremium',
            options={'verbose_name': 'نوع خاص', 'verbose_name_plural': 'پرمیوم\u200cها'},
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='features',
        ),
        migrations.AlterField(
            model_name='advertisementlocation',
            name='advertisement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='estate.advertisement', verbose_name='آگهی'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='typeGroup',
            field=models.CharField(choices=[('additionalFilters', 'ویژگی اضافی'), ('amenities', 'امکانات'), ('mainFeature', 'ویژگی اصلی')], max_length=50, verbose_name='نوع دسته\u200cبندی'),
        ),
        migrations.AlterField(
            model_name='secretadvertisement',
            name='advertisement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='estate.advertisement', verbose_name='آگهی'),
        ),
        migrations.AlterField(
            model_name='secretadvertisement',
            name='isFlagged',
            field=models.BooleanField(default=False, verbose_name='وضعیت آگهی مشکوک'),
        ),
        migrations.CreateModel(
            name='AdvertisementFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad_features', to='estate.advertisement', verbose_name='آگهی')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_ads', to='estate.feature', verbose_name='ویژگی')),
                ('value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estate.featurevalue', verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'ویژگی آگهی',
                'verbose_name_plural': 'ویژگی\u200cهای آگهی',
                'unique_together': {('advertisement', 'feature')},
            },
        ),
    ]
