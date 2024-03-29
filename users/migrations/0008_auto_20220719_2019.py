# Generated by Django 2.1.7 on 2022-07-20 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_background_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='github_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='stackoverflow_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='website_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]
