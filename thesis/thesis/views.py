import datetime
from django.template import loader
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import pyotp
from .utils import send_otp
from django.contrib.auth.models import User
from django.urls import reverse

import pymongo
connect_string='mongodb+srv://heroe:heroe@cluster0.wkxtx.mongodb.net/1christthesis?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['1christthesis']
collection_name = dbname["authentications_authentication"]




def login_view(request):
    error_message = None
    my_client = pymongo.MongoClient(connect_string)
    dbname = my_client['1christthesis']
    collection_name = dbname["authentications_authentication"]

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username: %s" % username, "password: %s" % password)
        # login_details = list(collection_name.find({
        #     "username":f"{username}"}))
        login_details = list(collection_name.find({"username":f"{username}"}))
        print("login_details: %s" % login_details, "password: %s" % password)

        if len(login_details):
            # details_client = login_details.pop()
            # print("details_client", details_client)
            return redirect('scrapping',id_client=1)
        else:
            error_message = 'Invalid username or password'
    return render(request, "login.html", {'error_message': error_message})

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST.get('otp')
        username = request.session["username"]

        otp_secret_key = request.session["otp_secret_key"]
        otp_valid_until = request.session["otp_valid_until"]
        
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)
            
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session["otp_secret_key"]
                    del request.session["otp_valid_until"]

                    return redirect('main')
                else:
                    error_message = 'Invalid OTP'
            else:
                del request.session["otp_secret_key"]
                del request.session["otp_valid_until"]
                error_message = 'OTP expired'
        else:
            error_message = 'ups... something went wrong'
    return render(request, "otp.html", {'error_message': error_message})
                
        
@login_required
def main_view(request):
    if 'username' in request.session:
        del request.session['username']
    return render(request, "main.html", {})

def logout_view(request):
    logout(request)
    return redirect('login')


def scrapping_view(request, id_client):
    print("request: ", request)
    return HttpResponse(f'THis is the order which its id is {id_client}.')
    return render(request, "scrapping.html", {})
