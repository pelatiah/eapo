# Generated by Django 3.2.4 on 2021-06-07 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services_app', '0002_auto_20210607_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.FloatField(default=0)),
                ('expenses', models.FloatField(default=0)),
                ('Note', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('validate_conter_offer', models.BooleanField(default=False)),
                ('conter_offers_counter', models.IntegerField(default=2)),
                ('not_accepted', models.BooleanField(default=False)),
                ('custom_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_custom_service', to='services_app.customservice', verbose_name='custom Service Offer')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services_app.customer')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_location', to='services_app.location', verbose_name='location Offer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_oreder', to='services_app.order', verbose_name='order Offer')),
                ('order_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_order_service', to='services_app.orderservice', verbose_name='service Offer')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='ExtraTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=10)),
                ('contract_person', models.CharField(default='', max_length=100)),
                ('description', models.TextField()),
                ('lebal', models.FloatField()),
                ('expenses', models.FloatField()),
                ('upload_file_if_any', models.FileField(blank=True, null=True, upload_to='files')),
                ('extra_note', models.TextField(blank=True, null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('upload_files', models.FileField(blank=True, null=True, upload_to='files')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveryLocation', to='services_app.location')),
            ],
        ),
    ]
