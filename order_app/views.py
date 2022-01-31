from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import(
    CustomService,
    OrderService,
    Order,
    Location,
    Offer,
    DeliveryBook,
    ExtraTask,
    Customer,
    LocationOrder
)

from django.contrib import messages
from services_app.views import send_email
import random, string
from .forms import (
    OfferForm,
    EditeOfferForm,
    ExtraTaskForm,
    EditeExtraTaskForm,
)
from services_app.forms import EditLocationForm, EditSiteAddForm, EditcontarctPerForm
from services_app.models import SiteAddresse, ContactPerson
from services_app.views import get_categories


@login_required
def my_orders_view(request):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    offers_qs = Offer.objects.filter(customer=customer)
    if offers_qs.exists():
        offer = offers_qs[0]
        if offer.accepted:
            if offer.order:

                # I charge the 'completed = True' to False and the issue with refreshing order page that mark location as completed was resolved
                offer.order.complated = False
                offer.order.save()
                for service in offer.order.custom_services:
                    for location in service.location.all():
                        location.accepted = True
                        location.completed = False
                        location.save()

                for service in offer.order.services:
                    for location in service.location.all():
                        location.accepted = True
                        location.completed = False
                        location.save()

            if offer.order_service:
                for location in offer.order_service.location.all():
                    location.accepted = True
                    location.completed = False
                    location.save()
            if offer.custom_service:
                for location in offer.custom_service.location.all():
                    location.accepted = True
                    location.completed = False
                    location.save()

            if offer.location:
                offer.location.accepted = True
                offer.location.completed = False
                offer.location.save()

    my_orders = Order.objects.filter(customer=customer, orderd=True)
    orders_list = []
    locations_count = 0
    for order in my_orders:
        count_of_items = order.services.count() + order.custom_services.count()
        order_services = order.services.all()
        custom_services = order.custom_services.all()
        locations_count = 0
        for os in order_services:
            locations_count += os.location.filter(accepted=False).count()
        for cs in custom_services:
            locations_count += cs.location.filter(accepted=False).count()

        offer = None
        try:
            offer = order.my_oreder.get()
        except:
            pass

        orders_list.append([order, count_of_items, locations_count, offer])

    context = {
        'my_orders': my_orders,
        'orders_list': orders_list,
        'locations_count': locations_count,
    }
    return render(request, 'order_app/my_orders.html', context)


@login_required
def edit_orderd_location_view(request, pk, item, the_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(
        customer=customer,
        id=pk,
    )
    site_addresses = SiteAddresse.objects.filter(customer=customer)
    contact_persons = ContactPerson.objects.filter(customer=customer)

    if location_qs.exists():

        location = location_qs[0]
        selected_site_add = None
        selected_contract_person = None
        try:
            selected_site_add = location.site_addresse.all()[0]
        except:
            pass
        try:
            selected_contract_person = location.contact_person.all()[0]
        except:
            pass
        form = EditLocationForm(instance=location)
        if request.method == "POST":
            form = EditLocationForm(request.POST, instance=location)
            my_site_add = request.POST.get('my_site_add')
            my_contact_person = request.POST.get('my_contact_person')
            site_name = request.POST.get('site_name')

            new_contract_person = ContactPerson.objects.get(customer=customer, id=my_contact_person)
            new_site_add = SiteAddresse.objects.get(customer=customer, id=my_site_add)

            if form.is_valid():
                location = form.save(commit=False)
                location.edited = True
                location.customer = customer
                if selected_site_add:
                    location.site_addresse.remove(selected_site_add)
                location.site_addresse.add(new_site_add)
                if selected_contract_person:
                    location.contact_person.remove(selected_contract_person)
                location.contact_person.add(new_contract_person)

                location.save()

                messages.success(request, 'The location is successfully edited.')
                if the_type == '1':
                    return redirect(f'/detail-ordered-service/{item}/')
                return redirect(f'/detail-ordered-custum-service/{item}/')

        context = {
            'form': form,
            'site_addresses': site_addresses,
            'item': pk,
            'contact_persons': contact_persons,
            'selected_site_add': selected_site_add,
            'selected_contract_person': selected_contract_person

        }
        return render(request, "services_app/edite_location.html", context)
    else:
        messages.warning(request, 'The location is not exists.')
        return redirect('locationlist')


def delete_orderd_location_view(request, pk, service_pk, the_type=None):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    ordered_service = None

    try:
        ordered_service = OrderService.objects.get(customer=customer, id=service_pk, orderd=True)
    except:
        try:
            ordered_service = CustomService.objects.get(customer=customer, id=service_pk, orderd=True)
        except:
            pass

    if ordered_service:
        location_qs = Location.objects.filter(customer=customer, id=pk)
        if location_qs.exists():
            location = location_qs[0]
            ordered_service.location.remove(location)
            ordered_service.save()

            order_qs = Order.objects.filter(customer=customer, orderd=True)
            order_id = None
            for o in order_qs:
                if ordered_service in o.custom_services.all() or ordered_service in o.services.all():
                    order_id = ordered_service.id
                    break

            messages.success(request, 'The location is successfully removed.')
            if the_type == '2':
                return redirect(f'/detail-ordered-custum-service/{order_id}')
            return redirect(f'/detail-ordered-service/{order_id}')
        else:
            messages.warning(request, 'The location is Note exists')
            return redirect('locationlist')
    else:
        messages.warning(request,
                         'You can not access this page unless the service you wanna remove a location to exists..')
        return redirect('cart')


@login_required
def selected_order_service_info_view(request, pk):
    """ this view handel  """
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    global_services_by_category_list = get_categories()

    context = {
        'global_services_by_category_list': global_services_by_category_list,
        'item': pk,
    }

    try:
        ordered_service = OrderService.objects.get(id=pk)
        context.update({
            'service': ordered_service,
            'location_count': ordered_service.location.all().count()
        })
    except:
        pass
    return render(request, 'order_app/edite_order_info.html', context)


@login_required
def delete_orderd_service_view(request, pk, order_pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    service = None
    try:
        service = OrderService.objects.get(id=pk, orderd=True, customer=customer)
    except:
        try:
            service = CustomService.objects.get(id=pk, orderd=True, customer=customer)
        except:
            messages.warning(request, 'this service is not exists')
            return redirect(f'/edit-order/{order_pk}/')

    order_qs = Order.objects.filter(customer=customer, orderd=True, id=order_pk)
    if order_qs.exists():
        order = order_qs[0]
        if not order.services.filter(id=service.id).exists() and not order.custom_services.filter(
                id=service.id).exists():
            messages.warning(request, 'this service is not in your order.')
            return redirect(f'/edit-order/{order_pk}/')
        elif order.services.filter(id=service.id).exists():
            order.services.remove(service)
            order.save()
            service.delete()

        else:
            order.custom_services.remove(service)
            order.save()
            service.delete()

        if len(order.services.all()) + len(order.custom_services.all()) < 1:
            order_qs.delete()
            messages.success(request, 'this service is removed from your order successfuly.')
            return redirect('my_orders')
        else:
            messages.success(request, 'this service is removed from your order.')
            return redirect(f'/edit-order/{order_pk}/')

    else:
        messages.warning(request, 'The order you trying to remove service from is not exists.')
        return redirect('my_orders')


@login_required
def cancel_order_view(request, pk):
    """ this view handel the cancelation of orders """
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    context = {}
    order_qs = Order.objects.filter(customer=customer, id=pk, complated=False)
    if order_qs.exists():
        order = order_qs[0]
        context.update({
            'order': order,
            'order_custom_services': order.custom_services.all()
        })
        if request.method == 'POST':
            order_qs.delete()
            if customer.user:
                subject = 'response to your order cancelation'
                message = f"""Hello Mr {customer.user.username} your order is successfuly canceld,
                        thanks and best regards"""
                send_email(subject, message, customer.user.email)

            messages.success(request, "you have successfully cancel your order.")
            return redirect('my_orders')
    else:
        messages.warning(request, "this order is not exists.")
        return redirect('my_orders')

    return render(request, 'order_app/cancel.html', context)


def order_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_qs = Order.objects.filter(customer=customer, id=pk)
    if order_qs.exists():
        order = order_qs[0]
        order_services = order.services.all()
        custom_services = order.custom_services.all()
        locations_count = 0
        for os in order_services:
            locations_count += os.location.filter(accepted=False).count()
        for cs in custom_services:
            locations_count += cs.location.filter(accepted=False).count()
        if locations_count < 1:
            messages.warning(request,
                             'This offer can not be submited because either this order has no locations or all it locations has accepted offers')
            return redirect('my_orders')

        form = OfferForm()
        if request.method == 'POST':
            form = OfferForm(request.POST)
            if form.is_valid():
                offer = form.save()
                offer.order = order
                offer.customer = customer
                offer.save()
                messages.success(request, 'Your offer is successfully submited')
                return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def cancel_order_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_qs = Order.objects.filter(customer=customer, id=pk)
    if order_qs.exists():
        order = order_qs[0]
        if order.my_oreder:
            offer = order.my_oreder.get().delete()
            messages.success(request, 'Your offer has successfully canceled')
            return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')


@login_required
def selected_custom_service_info_view(request, pk):
    """ this view handel  """

    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    global_services_by_category_list = get_categories()

    context = {
        'global_services_by_category_list': global_services_by_category_list,
        'item': pk,

    }

    try:
        service = CustomService.objects.get(id=pk)
        context.update({
            'service': service,
            'location_count': service.location.all().count()

        })
    except:
        pass
    return render(request, 'order_app/edite_custom_order_info.html', context)





def edite_order_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_qs = Order.objects.filter(customer=customer, id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.my_oreder:
            offer = order.my_oreder.get()
            form = EditeOfferForm(instance=offer)
            if request.method == 'POST':
                form = EditeOfferForm(request.POST, instance=offer)
                if form.is_valid():
                    offer = form.save()
                    offer.order = order
                    offer.customer = customer
                    offer.save()
                    messages.success(request, 'Your offer is successfully Edited')
                    return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def conter_order_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_qs = Order.objects.filter(customer=customer, id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.my_oreder:
            offer = order.my_oreder.get()
            if offer.conter_offers_counter > 0:
                form = EditeOfferForm(instance=offer)
                if request.method == 'POST':
                    form = EditeOfferForm(request.POST, instance=offer)
                    if form.is_valid():
                        offer = form.save()
                        offer.order = order
                        offer.validate_conter_offer = False
                        offer.conter_offers_counter -= 1
                        offer.customer = customer
                        offer.save()
                        messages.success(request, 'Your Conter offer is successfully sent')
                        return redirect('my_orders')
            else:
                offer.not_accepted = True
                offer.save()
                messages.warning(request, 'can not send offer anymore')
                return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def order_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_service_qs = OrderService.objects.filter(customer=customer, id=pk)
    if order_service_qs.exists():
        order_service = order_service_qs[0]

        locations_count = order_service.location.filter(accepted=False).count()
        if locations_count < 1:
            messages.warning(request,
                             'This offer can not be submited because either this service has no locations or all it locations has accepted offers')
            return redirect('my_orders')

        form = OfferForm()
        if request.method == 'POST':
            form = OfferForm(request.POST)
            if form.is_valid():
                offer = form.save()
                offer.order_service = order_service
                offer.customer = customer
                offer.save()
                messages.success(request, 'Your offer is successfully submited')
                return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def cancel_order_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_service_qs = OrderService.objects.filter(customer=customer, id=pk)
    if order_service_qs.exists():
        order_service = order_service_qs[0]
        if order_service.my_order_service:
            offer = order_service.my_order_service.get().delete()
            messages.success(request, 'Your offer has successfully canceled')
            return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')


def edite_order_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_service_qs = OrderService.objects.filter(customer=customer, id=pk)
    if order_service_qs.exists():
        order_service = order_service_qs[0]

        if order_service.my_order_service:
            offer = order_service.my_order_service.get()
            form = EditeOfferForm(instance=offer)
            if request.method == 'POST':
                form = EditeOfferForm(request.POST, instance=offer)
                if form.is_valid():
                    offer = form.save()
                    offer.order_service = order_service
                    offer.customer = customer
                    offer.save()
                    messages.success(request, 'Your offer is successfully Edited')
                    return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def conter_order_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_service_qs = OrderService.objects.filter(customer=customer, id=pk)
    if order_service_qs.exists():
        order_service = order_service_qs[0]

        if order_service.my_order_service:
            offer = order_service.my_order_service.get()
            if offer.conter_offers_counter > 0:
                form = EditeOfferForm(instance=offer)
                if request.method == 'POST':
                    form = EditeOfferForm(request.POST, instance=offer)
                    if form.is_valid():
                        offer = form.save()
                        offer.order_service = order_service
                        offer.validate_conter_offer = False
                        offer.conter_offers_counter -= 1
                        offer.customer = customer
                        offer.save()
                        messages.success(request, 'Your Conter offer is successfully sent')
                        return redirect('my_orders')
            else:
                offer.not_accepted = True
                offer.save()
                messages.warning(request, 'can not send offer anymore')
                return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def order_custom_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_custom_service_qs = CustomService.objects.filter(customer=customer, id=pk)
    if order_custom_service_qs.exists():
        order_custom_service = order_custom_service_qs[0]
        locations_count = order_custom_service.location.filter(accepted=False).count()
        if locations_count < 1:
            messages.warning(request,
                             'This offer can not be submited because either this service has no locations or all it locations has accepted offers')
            return redirect('my_orders')

        form = OfferForm()
        if request.method == 'POST':
            form = OfferForm(request.POST)
            if form.is_valid():
                offer = form.save()
                offer.custom_service = order_custom_service
                offer.customer = customer
                offer.save()
                messages.success(request, 'Your offer is successfully submited')
                return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def cancel_custom_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_custom_service_qs = CustomService.objects.filter(customer=customer, id=pk)
    if order_custom_service_qs.exists():
        order_custom_service = order_custom_service_qs[0]
        if order_custom_service.my_custom_service:
            offer = order_custom_service.my_custom_service.get().delete()
            messages.success(request, 'Your offer has successfully canceled')
            return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')


def edite_custom_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_custom_service_qs = CustomService.objects.filter(customer=customer, id=pk)
    if order_custom_service_qs.exists():
        order_custom_service = order_custom_service_qs[0]

        if order_custom_service.my_custom_service:
            offer = order_custom_service.my_custom_service.get()
            form = EditeOfferForm(instance=offer)
            if request.method == 'POST':
                form = EditeOfferForm(request.POST, instance=offer)
                if form.is_valid():
                    offer = form.save()
                    offer.custom_service = order_custom_service
                    offer.customer = customer
                    offer.save()
                    messages.success(request, 'Your offer is successfully Edited')
                    return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def conter_custom_service_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    order_custom_service_qs = CustomService.objects.filter(customer=customer, id=pk)
    if order_custom_service_qs.exists():
        order_custom_service = order_custom_service_qs[0]

        if order_custom_service.my_custom_service:
            offer = order_custom_service.my_custom_service.get()
            if offer.conter_offers_counter > 0:
                form = EditeOfferForm(instance=offer)
                if request.method == 'POST':
                    form = EditeOfferForm(request.POST, instance=offer)
                    if form.is_valid():
                        offer = form.save()
                        offer.custom_service = order_custom_service
                        offer.validate_conter_offer = False
                        offer.conter_offers_counter -= 1
                        offer.customer = customer
                        offer.save()
                        messages.success(request, 'Your conter offer is successfully sent')
                        return redirect('my_orders')
            else:
                offer.not_accepted = True
                offer.save()
                messages.warning(request, 'can not send offer anymore')
                return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            return redirect('my_orders')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def location_offer_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(customer=customer, id=pk)
    if location_qs.exists():
        location = location_qs[0]
        form = OfferForm()
        if request.method == 'POST':
            form = OfferForm(request.POST)
            if form.is_valid():
                offer = form.save()
                offer.location = location
                offer.customer = customer
                offer.save()

                messages.success(request, 'Your offer is successfully Edited')
                if f_type == "1":
                    return redirect(f'/detail-ordered-service/{item}')
                return redirect(f'/detail-ordered-custum-service/{item}')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def cancel_location_offer_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(customer=customer, id=pk)
    if location_qs.exists():
        location = location_qs[0]
        if location.my_location:
            offer = location.my_location.get().delete()
            messages.success(request, 'Your offer has successfully canceled')
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')
        else:
            messages.warning(request, 'Your order has no offers')
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')


def edite_location_offer_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(customer=customer, id=pk)
    if location_qs.exists():
        location = location_qs[0]

        if location.my_location:
            offer = location.my_location.get()
            form = EditeOfferForm(instance=offer)
            if request.method == 'POST':
                form = EditeOfferForm(request.POST, instance=offer)
                if form.is_valid():
                    offer = form.save()
                    offer.location = location
                    offer.customer = customer
                    offer.save()
                    messages.success(request, 'Your offer is successfully Edited')
                    if f_type == "1":
                        return redirect(f'/detail-ordered-service/{item}')
                    return redirect(f'/detail-ordered-custum-service/{item}')
        else:
            messages.warning(request, 'Your order has no offers')
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def conter_location_offer_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(customer=customer, id=pk)
    if location_qs.exists():
        location = location_qs[0]

        if location.my_location:
            offer = location.my_location.get()
            if offer.conter_offers_counter > 0:
                form = EditeOfferForm(instance=offer)
                if request.method == 'POST':
                    form = EditeOfferForm(request.POST, instance=offer)
                    if form.is_valid():
                        offer = form.save()
                        offer.location = location
                        offer.validate_conter_offer = False
                        offer.conter_offers_counter -= 1
                        offer.customer = customer
                        offer.save()
                        messages.success(request, 'Your conter offer is successfully sent')
                        if f_type == "1":
                            return redirect(f'/detail-ordered-service/{item}')
                        return redirect(f'/detail-ordered-custum-service/{item}')
            else:
                offer.not_accepted = True
                offer.save()
                messages.warning(request, 'can not send offer anymore')
                return redirect('my_orders')
        else:
            messages.warning(request, 'Your order has no offers')
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')

    context = {'form': form}
    return render(request, 'order_app/offers.html', context)


def accept_offer_view(request, pk):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    offer_qs = Offer.objects.filter(customer=customer, id=pk)
    redirect_to = 0
    if offer_qs.exists():
        offer = offer_qs[0]
        offer.accepted = True
        offer.validate_conter_offer = False
        offer.save()
        if offer.order:
            for service in offer.order.custom_services:
                for location in service.location.all():
                    location.accepted = True
                    location.completed = False
                    location.save()

            for service in offer.order.services:
                for location in service.location.all():
                    location.accepted = True
                    location.completed = False
                    location.save()

        if offer.order_service:
            for location in offer.order_service.location.all():
                location.accepted = True
                location.completed = False
                location.save()
        if offer.custom_service:
            for location in offer.custom_service.location.all():
                location.accepted = True
                location.completed = False
                location.save()
        messages.success(request, 'Congrats your offer is successfully accepted')
        return redirect('my_orders')

    else:
        messages.warning(request, 'This offer is not exists')
        return redirect('my_orders')


def accept_location_offer_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    offer_qs = Offer.objects.filter(customer=customer, id=pk)
    redirect_to = 0
    if offer_qs.exists():
        offer = offer_qs[0]
        if offer.location.edited:
            messages.warning(request, 'This offer can not be accepted because the location edit is not confirmed yet')
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')

        offer.accepted = True
        offer.validate_conter_offer = False
        offer.save()

        # this is were we make deliverable invisible when offer was accepted
        offer.location.accepted = True
        offer.location.completed = False
        offer.location.save()

        if f_type == "1":
            return redirect(f'/detail-ordered-service/{item}')
        return redirect(f'/detail-ordered-custum-service/{item}')
    else:
        messages.warning(request, 'This offer is not exists')
        return redirect('my_orders')


def add_extra_tasks_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    # The line below resolve the the following error 'local variable 'form' referenced before assignment'
    #form = ExtraTaskForm()
    location_qs = LocationOrder.objects.filter(customer=customer, id=pk)
    if location_qs.exists():
        location = location_qs[0]
        form = ExtraTaskForm()
        if request.method == 'POST':
            form = ExtraTaskForm(request.POST or None)
            if form.is_valid():
                task = form.save()
                task.customer = customer
                task.save()
                location.extra_tasks.add(task)
                location.save()

                messages.success(request,
                                 'your task is under review it will be shown in your dashboard after it gets confirmed')
                if f_type == "1":
                    return redirect(f'/detail-ordered-service/{item}')
                return redirect(f'/detail-ordered-custum-service/{item}')

    context = {'form': form, }
    return render(request, 'order_app/extra_tasks.html', context)


def edite_extra_tasks_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    task_qs = ExtraTask.objects.filter(customer=customer, id=pk)
    if task_qs.exists():
        task = task_qs[0]
        # the line below does not permit me to modify extra task edith and delete after I rearrange the html
        # if task.confirmed:
        if task:
            form = EditeExtraTaskForm(instance=task)
            if request.method == 'POST':
                form = ExtraTaskForm(request.POST, instance=task)
                if form.is_valid():
                    task = form.save()

                    messages.warning(request, 'your task is successfully edited')

                    if f_type == "1":
                        return redirect(f'/detail-ordered-service/{item}')
                    return redirect(f'/detail-ordered-custum-service/{item}')
        else:
            messages.warning(request, 'This task is not confirmed yet')
            return redirect('my_orders')

    context = {'form': form, }
    return render(request, 'order_app/extra_tasks.html', context)


def delete_extra_tasks_view(request, pk, item, f_type):
    try:
        customer = request.user.customer
    except:
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    task_qs = ExtraTask.objects.filter(customer=customer, id=pk)
    if task_qs.exists():
        task = task_qs[0]

        if task.confirmed:
            task.delete()
            if f_type == "1":
                return redirect(f'/detail-ordered-service/{item}')
            return redirect(f'/detail-ordered-custum-service/{item}')
        else:
            messages.warning(request, 'This task is not confirmed yet')
            return redirect('my_orders')

    context = {'form': form, }
    return render(request, 'order_app/extra_tasks.html', context)



def delivery_book_view(request, pk):
    try:
        customer = request.user.customer
    except :
        device_id = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device_id=device_id)

    location_qs = Location.objects.filter(customer=customer, id=pk)
    delivery_book = None
    if location_qs.exists():
        location = location_qs[0]
        delivery_book_qs = DeliveryBook.objects.filter(location=location)
        if delivery_book_qs.exists():
            delivery_book = delivery_book_qs[0]
        else:
            pass
    else:
        pass
    context = {
        'delivery_book':delivery_book,
    }
    return render(request, 'order_app/delivery_book.html', context)

