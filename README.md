# Main README
To install and run this webapp, you must install pipenv on your machine to deal with dependencies, as well as python 3.9.
To do this from the command line run pip install pipenv

Once installed, navigate to the directory with the pipfile, and, again on the command line, run:
pipenv update
This will generate the lock file and download the required dependencies.

To run the app locally, navigate to the folder with the manage.py file, and run 
pipenv shell (this will open the environment containing the dependencies)
python manage.py runserver (this will begin running the django development server)