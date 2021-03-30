# Main README
NOTE: For information regarding the API, please check the readme located in cs30_Webapp/API/

Heroku:

The webapp should be deployed to https://cs30.herokuapp.com with dummy data so you can see how it works.

Running locally:

To install and run this Webapp, you must install pipenv on your machine to deal with dependencies, as well as python 3.9.
To do this from the command line run pip install pipenv

Once installed, navigate to the directory with the pipfile, and, again on the command line, run:
pipenv update
This will generate the lock file and download the required dependencies.

To run the app locally, edit settings.py as described at the bottom of this file,
navigate to the folder with the manage.py file, and run:
pipenv shell (this will open the environment containing the dependencies)
python manage.py runserver (this will begin running the django development server)

Next, navigate to http://127.0.0.1:8000. You will be greeted with the Webapp's homepage.



Normal Use:

You will only be able to make use of the Webapp if you are logged into an
account that has been marked as staff by an admin. A default admin account has been supplied:
Username: admin
Password: admin

It is highly reccomended you delete this account as soon as a new admin account is created.
With this account you can activate access the Webapp, and activate any created accounts. This can be done by marking them
as staff on their account page. The can be done by navigating from: home -> admin -> users, then selecting the account
you want to enable, and ticking the staff status check-box, before scrolling to the bottom of the page and selecting save.
New admin accounts can also be created in this way, by ticking superuser status rather than staff status.

An alternative method to create a new admin account is to run the following from the same directory manage.py can be found, just as the
server is run above:
python manage.py createsuperuser

User accounts also can be deleted from the user page, checking the boxes to the left of each user you want to delete before selecting
'delete selected users' from the action dropdown and clicking 'Go'.

Once you are signed into a valid account, you can access a view of the full database, a page to edit a selected entry,
an upload page to add a new entry of file, and a search to find specific entries by their ID or a group of entries by a keyword.

An example database file has been provided in the top directory of this project called TESTFILE.xlsx, displaying the format any uploaded file should follow, as well as being detailed in the pop-up on the upload page.



Further Development:

If a search results in a 'Search contained illegal characters, please try another.' message but should have returned a valid list of entries, the search may have been out bounds of the regex in api/urls.py due to updates in the way the database was formatted, or use of special characters to denote some new information. This can be fixed simply by updating the regex and redeploying the API.


The URL used in views.py, 'http://cs30.herokuapp.com/API/carbon', is specific to the deploy location used for development and final delivery. Should you wish to deploy it elsewhere this will need to be changed.


Running the Webapp locally will require some changes to settings.py.
DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']

The above lines should be changed as below to allow local development:

DEBUG = True
ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1']

They should however be kept as initially shown for deployment, substituting '.herokuapp.com'
with the host-name of the location the Webapp is being deployed.

Currently, the data is stored on a mongodb ATLAS server, this was mainly for development purposes, to change the database used by the webapp, the code can be found in settings.py for the main project, with the main admin account for the server logged there too

The section of code below, located in settings.py, may need to be commented out for local development depending on browser.

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

As before, ensure this change is reverted for deployment.

Note: In parts of the API, there are security vulnearbilities that we did not have the time to address, these are outlined further in the api readme.md
