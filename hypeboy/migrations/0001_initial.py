# Generated by Django 4.1.5 on 2023-05-20 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(default='', max_length=200)),
                ('weight', models.CharField(default='0', max_length=100)),
                ('count', models.IntegerField(default=0)),
                ('set', models.IntegerField(default=0)),
                ('completion', models.IntegerField(default=0)),
                ('total_completion', models.IntegerField(default=0)),
                ('view_yn', models.IntegerField(default=1)),
                ('start_date', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
    ]
