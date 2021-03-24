# Main README
To install and run this webapp, you must install pipenv on your machine to deal with dependencies, as well as python 3.9.
To do this from the command line run pip install pipenv

Once installed, navigate to the directory with the pipfile, and, again on the command line, run:
pipenv update
This will generate the lock file and download the required dependencies.

To run the app locally, navigate to the folder with the manage.py file, and run
pipenv shell (this will open the environment containing the dependencies)
python manage.py runserver (this will begin running the django development server)

Next, navigate to http://127.0.0.1:8000. You will be greeted with the webapp's homepage. You will only be able to
make use of the webapp if you are logged into an account that has been marked as staff by an admin. A default admin account has been supplied:
Username: admin
Password: admin
With this account you can activate access the webapp, and activate any created accounts. This can be done by marking them as staff on their account page. The can be done by navigating from: home -> admin -> users, then selecting the account you want to enable, and ticking the staff status checkbox
before scrolling to the bottom of the page and selecting save.
New admin accounts can also be created in this way, by ticking superuser status rather than staff status.
An alternative method to create a new admin account is to run the following from the same directory manage.py can be found, just as the
server is run above:
python manage.py createsuperuser

Once you are signed into a valid account, you can access a view of the full database, a page to edit a selected entry, an upload page to add a new
entry of file, and a search to find specific entries by their ID or a group of entries by a keyword.

An example database file has been provided in the top directory of this project called TESTFILE.xlsx, displaying the format any uploaded file should follow, as well as being detailed in the pop-up on the upload page.
