from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^', include('main.urls', namespace='main')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^robpuroxymatt/', admin.site.urls),
    url(r'^interface/', include('interface.urls', namespace='interface')),
    url(r'^interface/order/', include('orders.urls', namespace='order')),
    url(r'^interface/invoices/', include('invoices.urls', namespace='invoices')),
    url(r'^interface/services/', include('services.urls', namespace='services')),
    url(r'^interface/payment/', include('payments.urls', namespace='payments')),
    url(r'^interface/tickets/', include('tickets.urls', namespace='tickets')),
]

handler404 = 'interface.views.error_404'
handler500 = 'interface.views.error_500'
