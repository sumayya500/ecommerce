# Generated by Django 5.1.2 on 2024-11-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
