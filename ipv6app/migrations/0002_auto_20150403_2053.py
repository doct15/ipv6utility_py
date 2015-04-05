# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipv6app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prefix',
            name='flag',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='prefix',
            name='mask',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
