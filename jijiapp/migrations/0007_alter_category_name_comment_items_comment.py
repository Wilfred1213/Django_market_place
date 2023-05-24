# Generated by Django 4.0 on 2023-05-07 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jijiapp', '0006_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Agriculture', 'Agriculture'), ('Computer', 'Computers'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('School', 'School'), ('Tailor', 'Tailor'), ('Tools', 'Tools'), ('Phone', 'Phone'), ('Kitchen', 'Kitechen'), ('Ride', 'Ride'), ('Car', 'Cars'), ('Office', 'Office'), ('Food', 'Food'), ('Joweries', 'Joweries')], max_length=50),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('post_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jijiapp.comment'),
        ),
    ]
