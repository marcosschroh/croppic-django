from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        exclude = ('user',)


class CropProfilePictureForm(forms.Form):
    imgUrl = forms.URLField()
    imgInitW = forms.DecimalField()
    imgInitH = forms.DecimalField()
    imgW = forms.DecimalField()
    imgH = forms.DecimalField()
    imgX1 = forms.DecimalField()
    imgY1 = forms.DecimalField()
    cropW = forms.DecimalField()
    cropH = forms.DecimalField()
    rotation = forms.IntegerField()
