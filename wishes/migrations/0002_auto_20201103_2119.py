# Generated by Django 3.1.3 on 2020-11-03 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='age',
        ),
        migrations.RemoveField(
            model_name='member',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='price',
        ),
        migrations.AddField(
            model_name='member',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]