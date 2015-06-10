# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='time',
            field=models.CharField(default=datetime.datetime(2015, 6, 10, 6, 43, 16, 214575, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
