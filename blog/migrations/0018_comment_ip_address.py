# Generated by Django 2.1.7 on 2022-10-11 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_like_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ip_address',
            field=models.CharField(blank=True, default='00.000.000.000', max_length=25, null=True),
        ),
    ]
