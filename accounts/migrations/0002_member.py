# Generated by Django 4.1.5 on 2023-01-14 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='Members', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_id', models.IntegerField(default=0, null=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=100)),
                ('user_type', models.SmallIntegerField(null=True)),
                ('trainer_group', models.IntegerField(default=0)),
                ('user_height', models.FloatField(null=True)),
                ('user_weight', models.FloatField(null=True)),
                ('user_status', models.SmallIntegerField(default=1)),
                ('user_view', models.SmallIntegerField(default=1)),
                ('user_gender', models.SmallIntegerField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True)),
            ],
        ),
    ]