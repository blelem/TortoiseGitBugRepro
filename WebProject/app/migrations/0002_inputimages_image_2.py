# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputimages',
            name='image_2',
            field=models.ImageField(default='', upload_to=b''),
            preserve_default=False,
        ),
    ]
