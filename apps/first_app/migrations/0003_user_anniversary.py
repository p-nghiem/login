# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-26 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='anniversary',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
