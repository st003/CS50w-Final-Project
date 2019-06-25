# CS50W Final Project

My CS50w final project is a web-based shopping cart for selling licenses of digital products. Customers may register an account, add products to their shopping cart, purchase product licenses, add users, and assign purchased licenses to those users.

The application is built with the Django and Bootstrap frameworks. The user model is extended from the default Django user model to take advantage of Django's built in authentication system. The entire user interface is mobile compatible.

## Description of Contents

* *purchasing/* - Top level directory for the purchasing app where core functionality resides.
* *purchasing/migrations/* - The migrations for the purchasing app.
* *purchasing/static/* - Images, styles, and scripts for the puchasing app.
* *purchasing/tempalates/* - Templates for the purchasing app.
* *purchasing/admin.py* - Django admin configuration.
* *purchasing/models.py* - App specific models.
* *purchasing/urls.py* - App specific urls.
* *purchasing/views.py* - App specific views.

* *saas_cart/* - Django project folder
* *saas_cart/settings.py* - Main project settings
* *saas_cart/urls.py* - Main project url configuration

* *manage.py* - Command line tool for Django projects
* *README.md* - This document. The thing you are literally reading right now.
* *requirements.txt* - List of application dependencies used by Pip.

## Built With

* [Python](https://www.python.org/) - Language interpreter
* [Django](https://www.djangoproject.com/) - Web framework
* [Bootstrap](https://getbootstrap.com) - CSS Library

## Authors

* **st003** - *Initial work*