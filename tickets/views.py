"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tickets.models import Ticket
from tickets.forms import NewTicketForm, CloseTicketForm, ReplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from interface.email import SendEmail


@login_required
def ticket_list(request):
    """
    Purpose: Retrieve ticket(s) associated to user
    :param request: incoming request
    :return: rendered HTML template with tickets
    """
    objects = Ticket.objects.filter(user=request.user)
    paginator = Paginator(object_list=objects, per_page=10)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(number=page)
    except PageNotAnInteger:
        tickets = paginator.page(number=1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    return render(request=request, template_name='tickets/list.html', context={
        'tickets': tickets,
        'page': page
    })


@login_required
def ticket_new(request):
    """
    Purpose: Create new ticket
    :param request: incoming request
    :return: rendered HTML template with form
    """
    if request.method == 'POST':
        form = NewTicketForm(user=request.user, data=request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = 'open'
            ticket.user = request.user
            ticket.save()
            ticket_data = {
                'first_name': ticket.user.first_name,
                'client': '{} {}'.format(ticket.user.first_name, ticket.user.last_name),
                'ticket_id': str(ticket.uuid),
                'priority': ticket.priority,
                'subject': ticket.subject,
                'message': ticket.message
            }
            SendEmail(
                subject='New Support Ticket',
                to_email=ticket.user.email,
                data=ticket_data,
                template='new-ticket',
                user=ticket.user
            ).send()
            admin_ticket_data = {
                'client': '{} {}'.format(ticket.user.first_name, ticket.user.last_name),
                'ticket_id': str(ticket.uuid),
                'priority': ticket.priority,
                'subject': ticket.subject,
                'message': ticket.message
            }
            SendEmail(
                subject='New PuroxyIO Order Notification',
                data=admin_ticket_data,
                template='new-ticket',
            ).notify_admins()
            messages.success(request=request, message='Your ticket has been successfully created.')
            return HttpResponseRedirect(redirect_to=reverse('tickets:list'))
        else:
            messages.error(request=request, message='Please check your ticket input.')
    else:
        form = NewTicketForm(user=request.user)
    return render(request=request, template_name='tickets/new.html', context={
        'form': form
    })


@login_required
def ticket_detail(request, uuid):
    """
    Purpose: Retrieve ticket detail associated to user
    :param request: incoming request
    :param uuid: ticket universally unique identifier
    :return: rendered HTML template with detailed ticket
    """
    ticket = get_object_or_404(klass=Ticket, uuid=uuid, user=request.user)
    if request.method == 'POST':
        form = CloseTicketForm(data=request.POST)
        if form.is_valid():
            ticket.status = 'closed'
            ticket.save()
            messages.info(
                request=request,
                message='Ticket successfully closed. You can reply to open it again!'
            )
    else:
        form = CloseTicketForm()
    return render(request=request, template_name='tickets/detail.html', context={
        'ticket': ticket,
        'responses': ticket.responses.order_by('-created'),
        'form': form
    })


@login_required
def ticket_reply(request, uuid):
    """
    Purpose: Process new ticket reply
    :param request: incoming request
    :param uuid: ticket universally unique identifier
    :return: rendered HTML template with ticket response
    """
    ticket = get_object_or_404(klass=Ticket, uuid=uuid, user=request.user)
    if request.method == 'POST':
        form = ReplyForm(data=request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ticket = ticket
            response.user = request.user
            response.save()
            ticket.status = 'client_response'
            ticket.save()
            reply_data = {
                'client': '{} {}'.format(ticket.user.first_name, ticket.user.last_name),
                'ticket_id': str(ticket.uuid),
                'priority': ticket.priority,
                'subject': ticket.subject,
                'message': response.message
            }
            SendEmail(
                subject='New Support Ticket Response',
                data=reply_data,
                template='new-ticket-response',
            ).notify_admins()
            messages.success(
                request=request,
                message='Thank you for your response.'
            )
            return HttpResponseRedirect(redirect_to=reverse('tickets:detail', kwargs={
                'uuid': ticket.uuid
            }))
        else:
            messages.error(request=request, message='Please enter a valid ticket response.')
    else:
        form = ReplyForm()
    return render(request=request, template_name='tickets/reply.html', context={
        'ticket': ticket,
        'responses': ticket.responses.order_by('-created'),
        'form': form
    })
