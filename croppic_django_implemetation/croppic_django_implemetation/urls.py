"""croppic_django_implemetation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='customers/upload_image.html')),
    url(r'^upload_profile_image/$', 'customers.ajax.upload_profile_image',
         name='upload_profile_image'),
    url(r'^crop_profile_image/$', 'customers.ajax.crop_profile_image',
         name='crop_profile_image'),
]

if settings.DEBUG:
    urlpatterns += patterns('', *[

        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT, 'show_indexes': True, }),

        # (r'^(?P<path>.*)$', 'django.views.static.serve', {
        #     'document_root': settings.STATIC_ROOT,
        #     'show_indexes': True,
        # })
    ])

if settings.DEBUG:
    urlpatterns += patterns('', *[

        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),

    ])