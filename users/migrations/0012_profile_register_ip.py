# Generated by Django 2.1.7 on 2022-10-07 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20220728_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='register_ip',
            field=models.CharField(blank=True, default='00.000.000.000', max_length=25, null=True),
        ),
    ]
