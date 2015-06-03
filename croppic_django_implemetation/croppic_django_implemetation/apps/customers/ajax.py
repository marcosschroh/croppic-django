import json
import random

from django.http import HttpResponse
from django.contrib.sites.models import get_current_site

from PIL import Image

from customers.models import Customer
from customers.forms import CropProfilePictureForm


@login_required
def upload_profile_image(request):

    fytuser = request.user
    current_site = get_current_site(request)
    domain = current_site.domain

    ctx = {}

    try:
        instance = Customer.objects.get(fytuser=fytuser)
        ctx = {
            "preload_image_url": "http://%s/%s" % (domain, instance.img.url),
        }

    except FytUserImage.DoesNotExist:
        instance = None
        logger.info("FytUserImage Does Not Exist.")

    if request.is_ajax():

        form = FytUserImageForm(request.POST or None, request.FILES or None, instance=instance)

        if form.is_valid():

            new_image_fytuser = form.save(commit=False)

            new_image_fytuser.fytuser = fytuser
            new_image_fytuser.is_profile_image = True
            new_image_fytuser.save()

            img = Image.open(new_image_fytuser.img)
            width, height = img.size

            response = {
                "status": "success",
                "url": "http://%s/%s" % (domain, new_image_fytuser.img.url),
                "width": width,
                "height": height
            }

            return HttpResponse(json.dumps(response), content_type="application/json")

        response = {
                "status": "error",
                "message": form.errors,
            }

        return HttpResponse(json.dumps(response), content_type="application/json")

    return render(request, "registration/upload_profile_picture.html", ctx)


def crop_profile_image(request):

    if request.is_ajax():

        response = {
            "status": "error",
        }

        try:
            fytuser = request.user
            fyt_user_image = FytUserImage.objects.get(fytuser=fytuser)

        except FytUserImage.DoesNotExist:
            logger.warning("FytUserImage Does Not Exist..")
            response["message"] = "FytUserImage Does Not Exist.."
            return HttpResponse(json.dumps(response), content_type="application/json")

        form = CropProfilePictureForm(request.POST or None)

        if form.is_valid():

            # your image path (the one we recieved after successfull upload)
            imgUrl = form.cleaned_data.get("imgUrl")

            # your image original width (the one we recieved after upload)
            imgInitW = int(form.cleaned_data.get("imgInitW"))

            # your image original height (the one we recieved after upload)
            imgInitH = int(form.cleaned_data.get("imgInitH"))

            # your new scaled image width
            imgW = int(form.cleaned_data.get("imgW"))

            # your new scaled image height
            imgH = int(form.cleaned_data.get("imgH"))

            # top left corner of the cropped image in relation to scaled image
            imgX1 = int(form.cleaned_data.get("imgX1"))

            # top left corner of the cropped image in relation to scaled image
            imgY1 = int(form.cleaned_data.get("imgY1"))

            # cropped image width
            cropW = int(form.cleaned_data.get("cropW"))

            # cropped image height
            cropH = int(form.cleaned_data.get("cropH"))

            rotation = form.cleaned_data.get("rotation") * -1

            size = (int(imgW), int(imgH))

            try:
                im = Image.open(fyt_user_image.img)
                im = im.resize(size)
                im = im.rotate(rotation)

                box = (imgX1, imgY1, imgX1 + cropW, imgY1 + cropH)

                im = im.crop(box)

                im.save(fyt_user_image.img.file.name)
            except IOError as e:
                logger.warning("cannot create thumbnail for", fyt_user_image.img)
                logger.exception(e)
                response["message"] = "cannot create thumbnail for"
                return HttpResponse(json.dumps(response), content_type="application/json")

            current_site = get_current_site(request)
            domain = current_site.domain
            r = random.random()

            response = {
                "status": "success",
                "url": "http://%s/%s?a=%s" % (domain, fyt_user_image.img.url, r),
            }

            return HttpResponse(json.dumps(response), content_type="application/json")

        #If the form is invalid, send its errors.
        response["message"] = form.errors

        return HttpResponse(json.dumps(response), content_type="application/json")

    return HttpResponse(status=400)