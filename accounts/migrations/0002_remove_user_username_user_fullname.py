# Generated by Django 4.1.5 on 2023-01-24 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(max_length=14, null=True),
        ),
    ]