from django.shortcuts import render
from django.http import HttpResponse
from webapp.forms import UserForm, EditForm, UploadForm
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
    return render(request, 'webapp/home.html')

@login_required
def edit(request, refnum):
    entry = requests.get('http://cs30.herokuapp.com/api/carbon/' + refnum).json()
    for format in('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S'):
        try:
            entry['other_info']['last_update'] = datetime.datetime.strptime(str(entry['other_info']['last_update']), format)
        except ValueError:
            pass

    if request.method == 'POST':
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():

            edit = {
                        'ref_num':refnum,
                        # While levels cannot be edited currently, I'm leaving this in as an example.
                        'navigation_info':{
                            'scope':request.POST.get('scope'),
                            'level1':request.POST.get('level1'),
                            'level2':request.POST.get('level2'),
                            'level3':request.POST.get('level3'),
                            'level4':request.POST.get('level4'),
                            'level5':request.POST.get('level5')
                            },
                        'calculation_info':{
                            'ef':float(request.POST.get('ef')),
                            'cu':request.POST.get('cu')
                            },
                        'other_info':{
                            'last_update':(datetime.datetime.now(tz=None)).__str__(),
                            'preference':int(request.POST.get('preference')),
                            'source':request.POST.get('source')
                            }
                    }

                    #onClick="window.location.reload()"
            try_edit = requests.put('http://cs30.herokuapp.com/api/carbon/' + refnum, json=edit)

            messages.success(request, 'Edit successful!')
            return redirect(reverse('webapp:edit', kwargs={'refnum':refnum}))

        else:
            messages.error(request, 'Edit unsuccessful, please check edits are valid and try again.')
            return redirect(reverse('webapp:edit', kwargs={'refnum':refnum}))
    else:
        edit_form = EditForm()

    return render(request, 'webapp/edit.html', context={'edit_form': edit_form,'entry':entry})



from openpyxl import load_workbook

@login_required
def add(request):

    if request.method == 'POST':

        if 'upload' in request.POST:
            upload_form = UploadForm()
            test = str(request.FILES['uploadfile'])
            wb = load_workbook(request.FILES['uploadfile'])
            ws = wb.active

            for idx, row in enumerate(ws.iter_rows()):
                if idx == 0 or idx == 1:
                    continue
                else:
                    if ws.cell(row = idx, column = 1).value == None:
                        break
                    else:
                        edit = {
                                    'ref_num':ws.cell(row = idx+1, column = 1).value,
                                    'navigation_info':{
                                        'scope':ws.cell(row = idx+1, column = 2).value,
                                        'level1':ws.cell(row = idx+1, column = 3).value,
                                        'level2':ws.cell(row = idx+1, column = 4).value,
                                        'level3':ws.cell(row = idx+1, column = 5).value,
                                        'level4':ws.cell(row = idx+1, column = 6).value,
                                        'level5':ws.cell(row = idx+1, column = 7).value
                                        },
                                    'calculation_info':{
                                        'ef':ws.cell(row = idx+1, column = 10).value,
                                        'cu':ws.cell(row = idx+1, column = 9).value
                                        },
                                    'other_info':{
                                        'last_update':(ws.cell(row = idx+1, column = 12).value).__str__(),
                                        'preference':ws.cell(row = idx+1, column = 11).value,
                                        'source':ws.cell(row = idx+1, column = 8).value
                                        }
                                }
                        try_upload = requests.post('https://cs30.herokuapp.com/api/carbon', json=edit)

            messages.success(request, 'Upload successful!')
            return render(request, 'webapp/add.html', context={'upload_form': upload_form})

        elif 'save' in request.POST:
            upload_form = UploadForm(request.POST)
            if upload_form.is_valid():
                refnum = request.POST.get('ref_num')
                upload = {
                            'ref_num':int(refnum),
                            'navigation_info':{
                                'scope':request.POST.get('scope'),
                                'level1':request.POST.get('Level1'),
                                'level2':request.POST.get('Level2'),
                                'level3':request.POST.get('Level3'),
                                'level4':request.POST.get('Level4'),
                                'level5':request.POST.get('Level5')
                                },
                            'calculation_info':{
                                'ef':float(request.POST.get('ef')),
                                'cu':request.POST.get('cu')
                                },
                            'other_info':{
                                'last_update':(datetime.datetime.now(tz=None)).__str__(),
                                'preference':int(request.POST.get('preference')),
                                'source':request.POST.get('source')
                                }
                        }

                for key, value in upload['navigation_info'].items():
                    if value == '':
                        upload['navigation_info'][key] = None

                try_upload = requests.post('https://cs30.herokuapp.com/api/carbon', json=upload)

                messages.success(request, 'Upload successful!')
                return render(request, 'webapp/add.html', context={'upload_form': upload_form})

            else:
                messages.error(request, 'Upload unsuccessful, please check inputs are valid and try again.')

    else:
        upload_form = UploadForm()

    return render(request, 'webapp/add.html', context={'upload_form': upload_form})


@login_required
def delete(request, refnum):
    if request.method == 'POST':
        requests.delete('http://cs30.herokuapp.com/api/carbon/' + refnum)
        return redirect(reverse('webapp:dbview'))
    return render(request, 'webapp/dbview.html', context = {'entries': entries})


import datetime
# This view serves 3 pages, view, edit and upload, these might need to be separate. edit will require a push request, upload will probably need to use the population script (are we completely deleting data in the database or updating?)
@login_required
def dbview(request):
    # The url here will need to be made more general so it doesn't need to be changed based on host, I don't remember how to do that though
    entries = requests.get('http://cs30.herokuapp.com/api/carbon').json()

    for entry in entries:

        for format in('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S'):

            try:
                entry['other_info']['last_update'] = datetime.datetime.strptime(str(entry['other_info']['last_update']), format)
            except ValueError:
                pass

    return render(request, 'webapp/dbview.html', context = {'entries': entries})


def register(request):
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

            messages.success(request, 'Thank you for registering! Please wait for a staff member to activate your account.')
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
    return render(request, 'webapp/register.html', context={'user_form': user_form})


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
                messages.error(request, 'Your account has not been activated, please contact a staff member.')
                return render(request, 'webapp/login.html')
        else:
            # Bad login details were provided. So we can't log the user in.
            # This print displays their username and password on the console, enable for debug only.
            #print(f"Invalid login details: {username}, {password}")

            messages.error(request, 'Username or password was incorrect, please try again.')
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
