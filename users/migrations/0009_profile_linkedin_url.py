# Generated by Django 2.1.7 on 2022-07-20 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220719_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]
