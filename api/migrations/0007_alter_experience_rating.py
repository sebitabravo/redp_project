# Generated by Django 5.1.4 on 2024-12-11 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='rating',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
