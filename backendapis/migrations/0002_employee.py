# Generated by Django 3.2.20 on 2023-08-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'employee',
            },
        ),
    ]