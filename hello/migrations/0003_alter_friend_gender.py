# Generated by Django 3.2.18 on 2023-04-03 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20220817_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='gender',
            field=models.BooleanField(null=True),
        ),
    ]
