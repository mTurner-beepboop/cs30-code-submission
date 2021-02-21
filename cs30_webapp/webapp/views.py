from django.shortcuts import render
from django.http import HttpResponse
from webapp.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import requests



def home(request):
    return render(request,'webapp/home.html')


#This view serves 3 pages, view, edit and upload, these might need to be separate. edit will require a push request, upload will probably need to use the population script (are we completely deleting data in the database or updating?)
def dbview(request):
    response = requests.get('http://localhost:8000/api/carbon') #The url here will need to be made more general so it doesn't need to be changed based on host, I don't remember how to do that though
    entries = response.json() #This line puts the response into a python dictionary

    return render(request,'webapp/dbview.html', {'entries': entries})


def register(request):
    registered = False
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()


            # Update our variable to indicate that the template
            # registration was successful.
            messages.success(request,'Thank you for registering!')
            return render(request, 'webapp/home.html')
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()


    # Render the template depending on the context.
    return render(request, 'webapp/register.html', context = {'user_form': user_form, 'registered': registered})

def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_staff:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('webapp:home'))
            else:
                # An inactive account was used - no logging in!
                messages.error(request,'Your account has not been activated, please contact a staff member.')
                return render(request, 'webapp/login.html')
        else:
            # Bad login details were provided. So we can't log the user in.

            #This print displays their username and password on the console, enable for debug only.
            #print(f"Invalid login details: {username}, {password}")

            messages.error(request,'Username or password was incorrect, please try again.')
            return render(request, 'webapp/login.html')

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'webapp/login.html')



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect("/webapp/")
