import os
import datetime

from django.utils.text import slugify


def get_upload_path(instance, filename):
    timestamp = slugify(unicode(datetime.datetime.now().isoformat() + "-"))

    return os.path.join(
        instance.UPLOAD_TO,
        timestamp + filename.replace(" ", "-")
    )
