# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=128)),
                ('mask', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('possible', models.IntegerField(default=0)),
                ('flag', models.CharField(max_length=128)),
            ],
        ),
    ]
