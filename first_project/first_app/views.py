from django.shortcuts import render
from first_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import View,TemplateView
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content,features= 'html.parser')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[0:-13] # removing footers

toi_news = []

for th in toi_headings:
    toi_news.append(th.text)

def index(request):
        return render(request,'mainindex.html', {'toi_news':toi_news})

toi_r = requests.get("https://timesofindia.indiatimes.com/sports")
toi_soup = BeautifulSoup(toi_r.content,features= 'html.parser')

toi_headings = toi_soup.find_all('a')

toi_headings = toi_headings[0:-13] # removing footers

toi_news = []

for th in toi_headings:
    toi_news.append(th.text)

def sports(request):
    return render(request,'sports.html', {'toi_news':toi_news})
class politics(TemplateView):
    template_name="politics.html"

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse("first_app:index"))


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)



        # Get info from "both" forms
        # It appears as one form to the user on the .html page


        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():



            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Check if they provided a profile picture


            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
                print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form= UserProfileInfoForm()
 # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'login.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('first_app:index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'mainindex.html', {})
