# Generated by Django 4.1.3 on 2023-01-14 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_prettynum_alter_userinfo_depart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='管理员账户名')),
                ('password', models.CharField(max_length=64, verbose_name='管理员账户密码')),
            ],
        ),
    ]