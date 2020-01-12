import configparser
import os
import re
import sys
from os import sep

from home import settings
from home.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")

__author__ = ''


def install():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
    print('Thanks for choosing Cypetulip\n')
    # First select directory for data
    data_dir = input("Please choose directory for storing shop data [/var/cypetulip/]: ")

    config = configparser.RawConfigParser()
    config.add_section('data')
    config.add_section('db')
    if data_dir:
        config.set('data', 'DATA_DIR', data_dir)
    else:
        config.set('data', 'DATA_DIR', '/var/cypetulip/')

    # Select database
    db_tech = input("Please choose database technologie\nOptions are [mysql,sqlite]: ")
    if db_tech:
        config.set('db', 'engine', db_tech)
    else:
        config.set('db', 'engine', 'sqlite')

    if 'mysql' in db_tech:
        name = input("Please choose database name : ")
        host = input("Please choose database host [localhost]: ")
        port = input("Please choose database port [3306]: ")
        user = input("Please enter database user:")
        pwd = input("Please enter database password:")
        config.set('db', 'host', host or 'localhost')
        config.set('db', 'port', port or '3306')
        config.set('db', 'user', user)
        config.set('db', 'pwd', pwd)
        config.set('db', 'name', name)
    print('Setting up database...')
    # Then select dir for static stuff

    # Then collect the static stuff

    # Then initialize database

    with open(BASE_DIR + sep + 'settings.conf', 'w') as configfile:
        config.write(configfile)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")

    from django.core.management import execute_from_command_line
    print('#######Initializing Database########')
    execute_from_command_line(['', 'makemigrations'])
    apps = settings.INSTALLED_APPS
    for app in apps:
        if 'django' not in app:
            execute_from_command_line(['', 'makemigrations', app])
    execute_from_command_line(['', 'migrate'])
    print('####Creating a superuser account####')
    execute_from_command_line(['', 'createsuperuser'])
    from django.contrib.auth.models import User
    from shop.models import Contact
    users = User.objects.all()
    for user in users:
        contact = Contact()
    # Then populate database for every app
    #
    # from django.core.management import execute_from_command_line
    #
    # execute_from_command_line(sys.argv)
    from cms.sql.init_data import populate_db as cms_populate
    from shop.sql.init_data import populate_db as shop_populate
    cms_populate()
    shop_populate()


def populate_permissions():
    rgx = re.compile(r'(?P<app_name>[a-zA-Z]+)')
    import django
    django.setup()

    from permissions.models import AppUrl, App
    from permissions.utils import show_urls
    from home.urls import urlpatterns
    urls = {}
    show_urls(urlpatterns, urls=urls)
    old_urls = AppUrl.objects.all().delete()
    for app, app_urls in urls.items():
        if len(app) > 2:
            app_name = rgx.search(app).group()

            app_instance = App(is_public=True, name=app_name) if len(
                App.objects.filter(name=app_name)) == 0 else App.objects.get(name=app_name)
            app_instance.save()
            for url_name, url in app_urls.items():
                # complete_url = ('/%s%s' % (app, url)).replace("^","")
                app_url = AppUrl(app=app_instance, name=url_name, url="/" + url.replace("^", ""))
                app_url.save()


def create_app_perms_for_user(username):
    import django
    django.setup()
    from django.contrib.auth.models import User
    from permissions.models import AppUrl, AppUrlPermission
    user = User.objects.get(username=username)
    for app_url in AppUrl.objects.all():
        perm = AppUrlPermission(url=app_url, user=user, post_access=True, get_access=True)
        perm.save()


if __name__ == "__main__":
    if sys.argv[1] == '--populateperms':
        populate_permissions()
    elif sys.argv[1] == '--grantaccess':
        create_app_perms_for_user(sys.argv[2])
    elif sys.argv[1] == '--install':
        install()
