# Generated by Django 2.2.7 on 2019-11-17 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirm_password',
        ),
    ]
