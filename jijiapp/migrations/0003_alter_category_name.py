# Generated by Django 4.0 on 2023-06-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jijiapp', '0002_category_icon_class_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Food', 'Food'), ('Agriculture', 'Agriculture'), ('Computer', 'Computers'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('School', 'School'), ('Tailor', 'Tailor'), ('Tools', 'Tools'), ('Phone', 'Phone'), ('Kitchen', 'Kitchen'), ('Ride', 'Ride'), ('Car', 'Cars'), ('Office', 'Office'), ('Jewelry', 'Jewelry')], max_length=50),
        ),
    ]
