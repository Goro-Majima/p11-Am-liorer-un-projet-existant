# P8-purbeurre

Application made by Mickael Ly in order to achieve a school project.

The purpose is to deploy a functionnal application for consumers willing to change their nutritional habits. 

The challenge is to build dynamic app with the framework Django in Python and fill a postgres db with datas from the Openfoodfacts APi with only using a django Orm instead of SQL.

## User Journey

Once on homepage, a user can easily find a product and get its substitute right at the next page. Details are its nutrigrade, nutrients, a link for more details about it.

He can register, sign in and add products in his profile if he really wants to save it for later use.


## Installation

```bash
pip install Django
pip install django-extensions
pip install django-crispy-forms
pip install django-debug-toolbar
pip install Pillow
pip install requests
```

Install Postgresql locally 

Don't forget to change password, name, variables if you rename your database info differently.

## Run

```python

python purbeurre/manage.py runserver

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
