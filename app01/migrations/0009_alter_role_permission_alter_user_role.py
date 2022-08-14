# Generated by Django 4.0.1 on 2022-01-30 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_alter_book_options_alter_role_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(related_name='permission', to='app01.Permissions', verbose_name='权限'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(related_name='role', to='app01.Role', verbose_name='角色'),
        ),
    ]