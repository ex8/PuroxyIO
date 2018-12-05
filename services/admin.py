"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from services.models import Service
from interface.email import SendEmail
from orders.models import Order
from dateutil.relativedelta import relativedelta


class ServiceAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Service admin pages
    """
    list_display = ('hostname', 'ip_address', 'next_due_date', 'control_panel', 'additional_ips', 'user')
    search_fields = ('hostname', 'ip_address', 'user')
    actions = ['service_detail_email', 'additional_ips_email']

    def service_detail_email(self, request, queryset):
        """
        Purpose: Send service detail email to respective user for each service in queryset
                 CAREFUL; this increments service.next_due_date for all products EXCEPT `web`
                          this is done in another place (payment/views.py)
        :param request: incoming request
        :param queryset: array of service objects ticked in ServiceAdmin list page
        :return: N/A
        """
        for service in queryset:
            order = Order.objects.get(service=service)
            if order.product.type == 'web':
                data = {
                    'first_name': service.user.first_name,
                    'product': order.product.name,
                    'hostname': service.hostname,
                    'cpanel_user': service.username,
                    'cpanel_password': service.password or 'Only you know this!',
                    'service_id': str(service.uuid)
                }
                SendEmail(
                    subject='cPanel Account Information',
                    to_email=service.user.email,
                    data=data,
                    template='cpanel-account-info',
                    user=service.user
                ).send()
            else:
                data = {
                    'first_name': service.user.first_name,
                    'product': order.product.name,
                    'hostname': service.hostname,
                    'main_ip_address': service.ip_address,
                    'server_username': service.username,
                    'server_password': service.password or 'Only you know this!',
                    'additional_ips_num': service.additional_ips,
                    'operating_system': service.os,
                    'control_panel': service.control_panel,
                    'service_id': str(service.uuid)
                }
                SendEmail(
                    subject='Your service is now online!',
                    to_email=service.user.email,
                    data=data,
                    template='service-detail-email',
                    user=service.user
                ).send()
                service.next_due_date += relativedelta(months=+1)
                service.save()
            self.message_user(request=request, message='Account information email sent.')
    service_detail_email.short_description = 'Email client account info for selected services'

    def additional_ips_email(self, request, queryset):
        """
        Purpose: Send additional ips email to respective user for each service in queryset
        :param request: incoming request
        :param queryset: array of service objects ticked in ServiceAdmin list page
        :return: N/A
        """
        for service in queryset:
            order = Order.objects.get(service=service)
            if order.product.type != 'web' and service.additional_ips_list is not None:
                data = {
                    'first_name': service.user.first_name,
                    'product': order.product.name,
                    'hostname': service.hostname,
                    'num': service.additional_ips,
                    'list': service.additional_ips_list,
                    'service_id': str(service.uuid)
                }
                SendEmail(
                    subject='Your Additional IP Address(es) have been deployed!',
                    to_email=service.user.email,
                    data=data,
                    template='additional-ips',
                    user=service.user
                ).send()
                self.message_user(request=request, message='Additional IPs email sent.')
    additional_ips_email.short_description = 'Email client additional ips info for selected services'


# Register model and admin class
admin.site.register(model_or_iterable=Service, admin_class=ServiceAdmin)
