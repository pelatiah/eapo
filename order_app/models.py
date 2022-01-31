from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
from django.conf import settings

from services_app.models import Customer, OrderService, Order, CustomService, Location

class DeliveryBook(models.Model):
    note = models.TextField()
    upload_files = models.FileField(upload_to='files', null=True, blank=True)
    # we will add approve and disapproved, this will allow the client to accept the deliverable or not
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='deliveryLocation')

    def __str__(self):
        return f'Id = {self.id} = {self.note[:30]}'

    @property
    def relative_path(self):
        return os.path.relpath(self.upload_files.path, settings.MEDIA_ROOT)


class ExtraTask(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    contract_person = models.CharField(max_length=100, default='')
    description = models.TextField()
    lebal = models.FloatField()
    expenses = models.FloatField()
    upload_file_if_any = models.FileField(upload_to='files', null=True, blank=True)
    extra_note = models.TextField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)


    def __str__(self):
        if self.customer.user :
            return f'Id = {self.id} = {self.customer.user.username} => {self.description[:40]}'
        else:
            return f'Id = {self.id} = {self.customer.device_id }'


class LocationOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='location Offer')
    extra_tasks = models.ManyToManyField(ExtraTask, blank=True)


    def __str__(self):
        if self.customer.user :
            return f'Id = {self.id} = {self.customer.user.username} => {self.location}'
        else:
            return f'Id = {self.id} = {self.customer.device_id} => {self.location}'


# Change the below class name to LocationOffer
class Offer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # the line below may have to be a standalone model, this will help us regarding the total labor which Location
    # offer + extra task/added task
    label = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    # we may include next line below to control added task
    #out_of_scope = models.ForeignKey(ExtraTask ,on_delete=models.SET_NULL, blank=True, null=True)
    Note = models.TextField(blank=True, null=True)
    # we might remove Order, order_service, custom_service from the model which may be included in their respective model
    order = models.ForeignKey(Order,related_name='my_oreder' ,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='order Offer')
    order_service = models.ForeignKey(OrderService, related_name='my_order_service' , on_delete=models.SET_NULL, blank=True, null=True, verbose_name='service Offer')
    custom_service = models.ForeignKey(CustomService,related_name='my_custom_service' ,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='custom Service Offer')
    location = models.ForeignKey(Location,related_name='my_location' , on_delete=models.SET_NULL, blank=True, null=True, verbose_name='location Offer')
    date = models.DateTimeField(auto_now_add=True)
    # eapo_acceptet = models.IntegerField()
    accepted = models.BooleanField(default=False)
    # we might include offer, which will allow us to make offer from our end
    validate_conter_offer = models.BooleanField(default=False)
    # I use 'editable' to hide conter_offer_counter so we don't alter the counteroffer rule
    conter_offers_counter = models.IntegerField(default=1)
    # not accepted should be hard and soft, when hard user cannot make offer anymore Unless we allow it from backend,
    # if soft he can start making offer from beginning
    not_accepted = models.BooleanField(default=False)
    #rate_per_hour = models.FloatField(min(25), default=25)
    #fixed_per_location = models.FloatField(min(25), default=25)
    #blended_rate = models.FloatField(min(25), default=25)
    #fixed_hours = models.FloatField(min(1), default=1)
    #first_hours = models.FloatField(min(1), default=1)
    #added_hours = models.FloatField(min(1), default=1)
    #max_hours = models.FloatField(min(1), default=1)


    class Meta:
        ordering = ('-date',)

    def __str__(self):
        if self.customer.user :
            return f'Id = {self.id} = {self.customer.user.username} offer'
        else:
            return f'Id = {self.id} = {self.customer.device_id}'


# There might be need for two more models 1) for service offer and the othe 2) for order offer