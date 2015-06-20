import json
import random

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PIL import Image

from .models import Customer
from .forms import CustomerForm, CropProfilePictureForm


def upload_profile_image(request):

    current_site = get_current_site(request)
    domain = current_site.domain
    user = User.objects.get()
    ctx = {}

    try:
        customer = Customer.objects.all().first()
        print "hola chiche"
        print domain
        if customer.img:
            ctx = {
                "preload_image_url": "http://%s/%s" % (domain, customer.img.url),
            }
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user)

    print "entrandooooo"

    if request.is_ajax():

        print "entrando al ajaxx"

        form = CustomerForm(request.POST or None, request.FILES or None)

        if form.is_valid():

            print "formulario validoo"
            customer = form.save(commit=False)

            customer.user = user
            customer.save()

            image = Image.open(customer.img)
            width, height = image.size

            response = {
                "status": "success",
                "url": "http://%s/%s" % (domain, customer.img.url),
                "width": width,
                "height": height
            }

            return HttpResponse(json.dumps(response))

        response = {
                "status": "error",
                "message": form.errors,
            }

        return HttpResponse(json.dumps(response), content_type="application/json")

    return render(request, "customers/upload_image.html", ctx)


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