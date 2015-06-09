from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$',  TemplateView(template_name='customers/upload_image.html'), name='customer_list'),
]
