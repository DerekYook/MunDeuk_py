# Generated by Django 5.0.6 on 2024-07-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startService', '0012_alter_memberinfo_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberinfo',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
