# Generated by Django 4.0.1 on 2022-01-29 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_user_role_alter_role_permission'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permission',
            new_name='Permissions',
        ),
    ]