from django.shortcuts import render

from customers.models import Customer


def all_customers(request):
    customers = Customers.objects.filter(user__is_active=True)

    ctx = {
		"customers": customers
	}
	
	return render(request, "customers/all_customers.html", ctx)
