# Generated by Django 4.1.3 on 2023-01-07 03:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hypeboy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='start_date',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='total_completion',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
    ]
