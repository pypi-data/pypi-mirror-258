ArtD Open Pay
=============
ArtD Open Pay It is a package that contains the Open Pay payment gateway for electronic commerce from the BBVA bank.
--------------------------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
        ...
        'artd_location',
        'artd_partner',
        'django-json-widget'
        'artd_customer'
        'artd_openpay'
    ]
``
2. Run python manage.py migrate to create the models.

3. Run the seeder data:
`python manage.py create_countries`
`python manage.py create_colombian_regions`
`python manage.py create_colombian_cities`