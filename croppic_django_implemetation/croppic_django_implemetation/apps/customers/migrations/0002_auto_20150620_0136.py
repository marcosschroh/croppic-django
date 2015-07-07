# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='img',
            field=models.ImageField(default=None, upload_to=utils.utils.get_upload_path, verbose_name=b'Image'),
            preserve_default=False,
        ),
    ]
