# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-12 03:31
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name=b'\xe5\x87\xba\xe7\x94\x9f\xe5\xb9\xb4\xe6\x9c\x88')),
                ('gender', models.CharField(choices=[(b'male', '\u7537'), (b'female', b'\xe5\xa5\xb3')], default=b'female', max_length=6, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('image', models.ImageField(default=b'', upload_to=b'users_avatar', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\xa4\xb4\xe5\x83\x8f')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('goods_sn', models.IntegerField(primary_key=True, serialize=False, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x94\xaf\xe4\xb8\x80\xe8\xb4\xa7\xe5\x8f\xb7')),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x90\x8d')),
                ('key', models.CharField(max_length=100, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x90\x9c\xe7\xb4\xa2\xe5\x85\xb3\xe9\x94\xae\xe8\xaf\x8d')),
                ('image', models.ImageField(max_length=200, upload_to=b'goods_image/')),
                ('priority', models.IntegerField(default=0, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbc\x98\xe5\x85\x88\xe7\xba\xa7')),
                ('file_address', models.CharField(max_length=100, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80')),
            ],
            options={
                'verbose_name': '\u5546\u54c1',
            },
        ),
    ]
