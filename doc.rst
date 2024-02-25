#############
Store Django Project Documentation
#############


Introduction
============

This project is a simple online store application built with Django. It allows users to see the products, purchase products,see orders above 3 million and see all people's orders by name. It also has features such as user authentication, shopping cart, checkout.

Installation
============

To install and run this project, you will need the following:

- Python 3.8 or later
- Django 5.0 or later
- A PostgreSQL database

You can install the required Python packages using pip::

    pip install -r requirements.txt

You will also need to create a PostgreSQL database and a user with full access to it. You can use the following commands as an example::

    sudo -u postgres psql
    CREATE DATABASE store;
    ALTER USER postgres PASSWORD '1234';

You will need to set the following environment variables with your database and Stripe credentials:

To initialize the database tables and create a superuser, you can run the following commands::


    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

To start the development server, you can run::

    python manage.py runserver

You can then access the application at http://localhost:8000.

Usage
=====

The application has two main parts: the public site and the admin site.

Public Site
-----------

The public site is where users can see products, buy products, see orders above 3 million and see all people's orders by name. It has the following pages:

- **/Store/list_product/**: This page displays a list of featured products.
- **/store/cart/**: The cart page shows the items that the user has added to their shopping cart, along with the total price and a checkout button.
- **/store/cart/add/<int:id>**: Adds the selected product to the card based on ID.
- **/store/user/order/<str:user>**: It shows all customer orders based on customer name.
- **/store/checkout**: The checkout page allows the user to enter their shipping and billing information.
- **/store/three/mil/**: The order page shows the details of the user's order, such as the order number, date, status, items, and tracking number. It also allows the user to cancel or return their order, or contact the seller.
- **Account**: The account page allows the user to view and edit their profile, change their password, and view their order history.
- **/account/login**: The login page allows the user to log in to their account using their email and password.
- **/account/logout**: The logout page logs the user out of their account and redirects them to the home page.
- **/account/signup**: Users can create their new account using this page.

Admin Site
----------

The admin site is where the site owner or staff can manage the products, categories, orders, users, and reviews. It can be accessed at http://localhost:8000/admin using the superuser credentials. It has the following sections:

- **Products**: The products section allows the admin to add, edit, or delete products, as well as upload image.
- **Categories**: The categories section allows the admin to add, edit, or delete categories, as well as assign products to them.
- **Orders**: The orders section allows the admin to view, edit, or delete orders.
- **Users**: The users section allows the admin to view, edit, or delete users, as well as assign them to groups or permissions.
- **Customers**: The customers section allows the admin to view, edit, or delete customers.

Deployment
----------
In this part, we will deploy the project on a Linux server using NGINX and UWSGI.
At first we need to install the required packages using the following codes:
::

    sudo apt-get update
    sudo apt-get install python3-pip nginx-full
    sudo -H pip3 install virtualenv
    sudo -H pip3 install uwsgi

Then we need to open the project in virtualenv:
::

    virtualenv -p python3 store<project name>
    source store/bin/activate

Now we need to install project dependencies:
::

    pip install -r store/requirements.txt

Now we need to set our domain as an allowed host for django so that we can use it so we need to go We need to go to the settings file in the store directory
and add our domain.
::

    vim store/store/setting.py

.. code-block:: python
    ALLOWED_HOSTS = ["127.0.0.1", "store.ir", "www.store.ir"]

Then we exit the virtualenv:
::

    deactivate

In the next step, we go to configure uwsgi as an application server.First, we need to create a file at
the following address for uwsgi settings.
::

    sudo mkdir -p /etc/uwsgi/sites
    sudo vim /etc/uwsgi/sites/store.ini

store.ini file settings:
.. code-block:: ini

    [uwsgi]
    project = store
    uid = <server-user>
    base = /home/<server-user>

    chdir = %(base)/%(project)
    home = %(base)/store
    module= %(project).wsgi:application

    master = true
    processes = 2

    socket = /run/uwsgi/%(project).sock
    chown-socket %(uid):www-data
    chmod-socket = 660
    vacuum = true

In the next step, we need to turn the uwsgi into a service:


    sudo vim /etc/systemd/system/uwsgi.service

.. code-block:: ini

    [Unit]
    Description=uWSGI Service

    [Service]
    ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown ubuntu:www-data'
    ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

Now we activate uwsgi service:
::

    sudo systemctl start uwsgi.service

It's time to configure Nginx To use Nginx, we need to create a virtual host. Virtual hosts allow us to manage several domains on one server:
::

    sudo vim/etc/nginx/sites/available/store.ir<project name>
.. code-block:: ini

    server {
        listen 80;
        server_name = store.ir www.store.ir;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /media/ {
                root    /var/www/store/;
        }
        location /static/ {
                root    /var/www/store/;
        }
        location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/store.sock;
    }
At last we need to make a symbolic link from available directory to sites-enabled:
::

    sudo ln -s /etc/nginx/sites/available/store.ir<project name> /etc/nginx/sites/sites-enabled

To use static files and media, we first create the following directories:
::

    sudo mkdir /var/www/store/
    sudo mkdir /var/www/store/static
    sudo mkdir /var/www/store/media
    sudo chown -R ubuntu:www-data /var/www/

Now we go back to the virtualenv to collect our statick files:
::

    source store/bin/activate
    python manage.py collectstatic
