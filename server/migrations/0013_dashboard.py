# Generated by Django 2.2.9 on 2021-01-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
