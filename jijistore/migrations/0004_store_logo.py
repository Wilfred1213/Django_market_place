# Generated by Django 4.0 on 2023-02-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jijistore', '0003_store_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='logo',
            field=models.ImageField(default='', upload_to='logos/'),
        ),
    ]