# Generated by Django 4.0 on 2023-03-11 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jijistore', '0005_alter_store_options_alter_store_create_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='store',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
    ]
