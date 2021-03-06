# PuroxyIO
PuroxyIO is a site and interface built in Django/Python. You may find images, features, and technologies used below. We have decided to release this software for educational purposes. We believe it is best used for this. We have built this system from scratch and have run numerous tests and quirks to put the finishing touches on it. This is the first main initial release. You can view the current, running site at www.puroxy.io.

### Features
- Everything can be controlled from the Django Admin itself, no need to dive into the code to add products/configurations unless you want to tweak it further
- Full source code is **heavily** documentated inline
- API Implementation (only includes GET requests at the moment)
- Fully working blogging system (SEO friendly slug URL's)
- Sparkpost Email integration seamlessly throughout entire site notifying both client and admins respectively
- More robust authentication middleware extending Django auth models/views
- Fully working billing system built from scratch (invoice renewals) -> used WHMCS Billing Logic (https://docs.whmcs.com/Billing_Logic)
- Invoice CronJob script that creates and suspends orders/services based on datetime expressions (ran daily)
- Main site is an app on its own
- Product Add-ons and Product Configuration fully abstracted and implemented, you can have different product configurations such as (hostname, operating systems, additional IP's, control panel, etc)
- Ordering is done mainly from Products and their respective configurations, easy to use implementation
-- This is built with the Product, ProductConfiguration, ProductConfigurationOption, and ProductConfigurationOptionItem models
- CoinPayments full integration for crypto-currency payment processing as well as PayPal integration, very secure system to ensure correct and assured requests arrive and send securely
- SolusVM integration to provide server operations on server instances
- WHM/cPanel integration to provide server operations and one-time click login on hosting instances
- Fully working ticketing/support system for clients/users to reach staff and admins

### Images
Dashboard
[![Dashboard](https://i.imgur.com/tohuUxj.png "Dashboard")](https://i.imgur.com/tohuUxj.png "Dashboard")

Ordering
[![Order](https://i.imgur.com/nsRMGwr.png "Order")](https://i.imgur.com/nsRMGwr.png "Order")

Services
[![Services](https://i.imgur.com/IZaXpZk.png "Services")](https://i.imgur.com/IZaXpZk.png "Services")

Payments
[![Payments](https://i.imgur.com/YBblTyc.png "Payments")](https://i.imgur.com/YBblTyc.png "Payments")

### Usage
Clone it. I recommend a virtualenv using python3, you can so with this command (change ENV_NAME to any python environment name you like): 
    `virtualenv -p python3 ENV_NAME`
    
Then activate the virtual environment like so:
	`source ENV_NAME/bin/activate`

Then you should see a (ENV_NAME) before your terminal shell name.
Then you need to install the dependencies like so:
	`pip install -r requirements.txt`

Then you can run the following commands to migrate and run the sever:
	`python manage.py makemigrations`
	`python manage.py migrate`
	`python manage.py runserver`

You should now be able to go to `localhost:8000`


### Main Technologies Used
- Django (of course)
- NGINX (reverse proxy)
- Gunicorn (wsgi web server)
- Django-crontab (cronjob)
- PostgreSQL (database)
- SparkPost (email)
- Django Rest Framework (api)
