# Little Lemon App

This project fulfills the requirement for Meta's [Back-End Developer Capstone course](https://www.coursera.org/learn/back-end-developer-capstone?specialization=meta-back-end-developer) on Coursera.

## Set-up instructions

**Note**: the virtual environment for this project uses the `pipenv` module. Make sure it is installed on your computer, otherwise run `pip install pipenv --user` to install
1. Navigate to the project directory in Bash or PowerShell `cd BEdev_Capstone/`
2. Run `pipenv install` to install all dependencies
3. Run `pipenv shell` to activate the virtual environment

### Database connection set-up
4. Create a database on the MySQL server running on your local machine and note down the `database_name`, `username` and `password`
5. Create a folder `mkdir littlelemon/mysql` and then create a file `touch littlelemon/mysql/my.cnf`
6. Paste the `database_name`, `username` and `password` credentials from step 4 into the `my.cnf` file in the following format (each value must be enclosed in single quotes):

```
[client]
database = 'database_name'
user = 'username'
password = 'password'
```
> **Alternative for step 5-6** Change the `settings.py` file in the project-level `littlelemon/littlelemon` folder as follows:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```
7. Run `python littlelemon/manage.py makemigrations` followed by `python littlelemon/manage.py migrate`

### Testing

8. Run `python littlelemon/manage.py runserver` to test the API endpoints and sites in your browser the root url is [http://localhost:8000]
9. To test APIs requiring authentication, use the `/auth/users/` endpoint to register a new user and get an api token from `/auth/token/login`
    * To test API functions requiring staff permissions, either register a superuser with `python littlelemon/manage.py createsuperuser` or go to the admin site [http://localhost:8000/admin/] and grant an existing user with staff permissions by setting `is_staff` to `True`.
10. Run `python littlelemon/manage.py test littlelemon/tests` to run the unit tests
11. Once testing is complete, run `exit` to terminate the virtual environment shell

## List of endpoints/routes

Endpoint                       | Type | Description
------------------------------ | ---- | -----------
`/admin/`                      | Site | For website administration
`/restaurant/`                 | Site | Home page of website
`/restaurant/about/`           | Site | About page of website
`/restaurant/menu/`            | Site | Menu page of website
`/restaurant/menu/<int:pk>`    | Site | See more details of particular menu item
`/restaurant/book/`            | Site | Form page to make a booking
`/restaurant/bookings/`        | API  | For querying and saving bookings to/from DB
`/restaurant/reservations/`    | Site | View all existing reservations in a table
`/auth/users/`                 | API  | From Djoser: user registration
`/auth/users/me/`              | API  | From Djoser: retrieve/update current user
`/auth/token/login`            | API  | From Djoser: get bearer token
`/restaurant/api-token-auth`   | API  | Alternative to get bearer token
`/auth/token/logout`           | API  | From Djoser: destroy bearer token
`/restaurant/booking/tables`   | API  | View existing bookings, add/delete existing bookings (authentication required - must be a registered user to book a table)
`/restaurant/api-menu/`        | API  | View entire menu, add menu item (must be staff user to add menu item)
`/restaurant/api-menu/<int:pk>`| API  | Retrieve, update/delete menu item (must be staff user to update or delete menu item)

## Improvements/changes made to basic specifications
- Database settings (username & password) stored in `littlelemon/mysql/my.cnf` file for better security
- Used `IsAuthenticatedOrReadOnly` permission class for `BookingViewSet` so that anyone can see bookings, but only registered users can add/change bookings
- Implemented validation of staff permission on `/restaurant/menu/` endpoints for operations that modify database
- Added more webpages to make the site complete

## Ways to further improve this project
- Modify the booking API and model so that only the user who created the booking can delete or change the booking
- Modify the booking API so that only the user's own bookin
- Add sign-in for webpage-based bookings
