from django.db import models
from django.contrib.auth.models import User

from utils.utils import get_upload_path


class Customer(models.Model):
    UPLOAD_TO = "customers/images"

    user = models.ForeignKey(User)
    imgage = models.ImageField("Image", upload_to=get_upload_path)

    def __unicode__(self):
        return "Full Name: %s %s" % (self.user.first_name, self.user.last_name)
