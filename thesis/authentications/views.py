
from django.shortcuts import render


from rest_framework.views import APIView


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from authentications.models import Authentication, History
from authentications.serializers import AuthenticationSerializer, HistorySerializer
from rest_framework.decorators import api_view

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.forms.models import model_to_dict

import datetime
from django.template import loader
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse       
from django.http import HttpResponseRedirect
from django.urls import reverse

import instaloader
from django.core import serializers
import requests
from bs4 import BeautifulSoup


class AuthenticationAPI(APIView):

    @api_view(['GET', 'POST', 'DELETE'])
    @extend_schema(responses=AuthenticationSerializer,
        parameters=[
            OpenApiParameter(name='artist', description='Filter by artist', required=False, type=str),
            OpenApiParameter(
                name='release',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filter by release date',
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='short optional summary',
                        description='longer description',
                        value='1993-08-23'
                    ),
                    ...
                ],
            ),
        ],
        # override default docstring extraction
        description='More descriptive text',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value=...
            ),
            ...
        ],
                   )
    def authentication_list(request):
        if request.method == 'GET':
            auths = Authentication.objects.all()
            password = request.GET.get('password', None)
            if password is not None:
                auths = auths.filter(password__icontains=password)
            
            auths_serializer = AuthenticationSerializer(auths, many=True)
            return JsonResponse(auths_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        elif request.method == 'POST':
            auth_data = JSONParser().parse(request)
            auth_serializer = AuthenticationSerializer(data=auth_data)
            if auth_serializer.is_valid():
                auth_serializer.save()
                return JsonResponse(auth_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            count = Authentication.objects.all().delete()
            return JsonResponse({'message': '{} we were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
    
    @api_view(['GET', 'PUT', 'DELETE'])
    @extend_schema(responses=AuthenticationSerializer)
    def authentication_detail(request, pk):
        try: 
            auth = Authentication.objects.get(pk=pk) 
        except Authentication.DoesNotExist: 
            return JsonResponse({'message': 'This account does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
        if request.method == 'GET': 
            auth_serializer = AuthenticationSerializer(auth) 
            return JsonResponse(auth_serializer.data) 
    
        elif request.method == 'PUT': 
            auth_data = JSONParser().parse(request) 
            auth_serializer = AuthenticationSerializer(auth, data=auth_data) 
            if auth_serializer.is_valid(): 
                auth_serializer.save() 
                return JsonResponse(auth_serializer.data) 
            return JsonResponse(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
        elif request.method == 'DELETE': 
            auth.delete() 
            return JsonResponse({'message': 'This account was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        
            
    @api_view(['GET'])
    
    @extend_schema(description='Override a specific method', methods=["GET"], parameters=[
            OpenApiParameter(name='artist', description='Filter by artist', required=True),
            OpenApiParameter(
                name='release',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filter by release date',
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='short optional summary',
                        description='longer description',
                        value='1993-08-23'
                    ),
                    
                ],
            ),
        ], 
                   examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value="sdsdsd"
            ),
        ],
                   )
    def authentication_list_is_superuser(request):
        auths = Authentication.objects.filter(is_superuser=True)
            
        if request.method == 'GET': 
            auths_serializer = AuthenticationSerializer(auths, many=True)
            return JsonResponse(auths_serializer.data, safe=False)
 

        user_client = Authentication.objects.get(id=id_client)
        if request.method == 'GET':
            try:
                auth_get = Authentication.objects.filter(id=id_client).values()
                history = History.objects.filter(email=auth_get[0]["email"]).values()
                history_serializer = HistorySerializer(history, many=True)
                return JsonResponse(history_serializer.data, safe=False, status=status.HTTP_200_OK)

            except:
                return JsonResponse({"data": ""}, status=status.HTTP_204_NO_CONTENT)

        if request.method == 'DELETE':
            
            try:
                auth_delete = History.objects.filter(email=user_client.email).delete()
                return JsonResponse({"result": True}, status=status.HTTP_200_OK) 

            except:
                return JsonResponse({"error_scrapping": "Something went wrong with id of user"}, status=status.HTTP_204_NO_CONTENT)

        return JsonResponse({"error_scrapping": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 
    

class ScrappingAPI(APIView):



    def login_view(request):

        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            print("username: %s" % username, "password: %s" % password)

            
            login_details = Authentication.objects.filter(email=username).values().first()
            print("login_details: %s" % login_details, "password: %s" % password)
            if login_details is not None:

                return redirect('scrapping',id_client=login_details["id"])

        return render(request, "login.html", {'error_message': 'Invalid username or password'})

    def signup_view(request):
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
        return render(request, "signup.html", {'error_message': error_message})
                    
            
    @login_required
    def main_view(request):
        if 'username' in request.session:
            del request.session['username']
        return render(request, "main.html", {})

    def logout_view(request):
        logout(request)
        return redirect('login')


    def scrapping_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        print("user_client: %s" % user_client.username)
        context ={ 'user': user_client}
        if request.method == 'POST':
             # FIRST FORM   
            user_typed = request.POST.get('user_typed')
            if user_typed: 
                bot = instaloader.Instaloader()
                cuenta=user_typed

                try:
                    profile_crapp = instaloader.Profile.from_username(bot.context, cuenta)
                    context["profile_crapp"] = profile_crapp
                    
                    user_history = History.objects.create(
                    hasUser=True,
                    email=user_client.email,
                    userId=id_client,
                    user_scrapping=user_typed,
                    web_scrapping=""
                )
                    user_history.save()                
                except:
                    context["error_user_scrapping"] = "Unknown User may you can try with another user"

            else:
                context["error_user_scrapping"] = "Unknown User"

             # SECOND FORM   
            web_typed = request.POST.get('web_typed')
            # another = request.POST.get('loco_typed')
            
            if web_typed and web_typed.lower().startswith('http'): 
                # url = "https://www.lamborghini.com/en-en"
                url = web_typed
                print("url", url)
                response = requests.get(url)
                if response.status_code == 200:

                    try:
                        soup = BeautifulSoup(response.content, "html.parser")
                        
                        links = soup.find_all("a")
                        data = []
                        for link in links:
                            data.append(link.get("href"))
                            # print(link.get("href"))
                        print("An exception occurred")
                        context["website_scrapping"] = data
                        
                        user_history = History.objects.create(
                        hasUser=True,
                        email=user_client.email,
                        userId=id_client,
                        user_scrapping="",
                        web_scrapping=web_typed,
                        )
                        user_history.save()                       
                    except:
                        context["error_web_scrapping"] = f"Website not reachable due to wrong website typed {web_typed}"


                    return render(request, "scrapping.html",  context)
                else:
                    context["error_web_scrapping"] = f"Website not reachable due to wrong website typed {web_typed}"
            else:
                context["error_web_scrapping"] = "Website not reachable due to wrong website typed valid with http: or https"
                
        return render(request, "scrapping.html", context)

    def scrapping_history_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        if user_client is not None:
            context={ "user": user_client}
            
            data_history = History.objects.filter(userId=id_client, email=user_client.email).values()


            # for i in data_history:
            #     print(i)
                            
            clean_data = []

            for i in data_history:
                item_data = {}
                if len(i['user_scrapping']) > 0:
                    item_data['user_scrapping'] = i['user_scrapping']
                if len(i['web_scrapping']) > 0:
                    item_data['web_scrapping'] = i['web_scrapping']
                if item_data:
                    clean_data.append(item_data)
            # for i in clean_data:
            #     print(i)
            
            context["data_history"] = clean_data
            return render(request, "history.html", context)
        else:
            context["error_message"] = "User provided does not exist"
            return render(request, "history.html", context)
    
    
class RESTScrappingAPI(APIView):
    @api_view(['POST'])
    def api_scrapping_user_view(request):
        # user_client = Authentication.objects.get(id=id_client)
        # print("user_client: %s" % user_client.username)
        # context ={ 'user': user_client}
        if request.method == 'POST':
            auth_data = JSONParser().parse(request)
            print("auth_data: ", auth_data)
            # user_typed = request.POST.get('user_typed')
            # print("user_typed:", user_typed)
            if auth_data["account"]: 
                # print("succeeded")
                bot = instaloader.Instaloader()
                # print("succeeded")
                # print("")
                cuenta=auth_data["account"]
                profile_crapp = instaloader.Profile.from_username(bot.context, cuenta)
                # print("Username: ", profile_crapp.username)
                # print("User ID: ", profile_crapp.userid)  
                # print("Number of Posts: ", profile_crapp.mediacount   )
                # print("Followers Count: ", profile_crapp.followers)   
                # print("Following Count: ", profile_crapp.followees)   
                # print("Bio: ", profile_crapp.biography)   
                # print("External URL: ", profile_crapp.external_url)
                # print(dir(profile_crapp))   
                # return JsonResponse(serializers.serialize('json', l), safe=True, status=status.HTTP_200_OK) 
                return JsonResponse({
                    "username": profile_crapp.username,
                    "userid": profile_crapp.userid,
                    "number_post": profile_crapp.mediacount,
                    "followers": profile_crapp.followers,
                    "biography": profile_crapp.biography,
                    "external_url": profile_crapp.external_url,
                        }, safe=True, status=status.HTTP_200_OK) 
            else:
                return JsonResponse({"error_scrapping": "Unknown User"}, status=status.HTTP_204_NO_CONTENT) 
        return JsonResponse({"error_scrapping": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 


    @api_view(['POST'])
    def api_scrapping_website_view(request):
        # user_client = Authentication.objects.get(id=id_client)
        # context ={ 'user': user_client}
        if request.method == 'POST':
            web_data = JSONParser().parse(request)

            if web_data["url"] and web_data["url"].lower().startswith('http'): 
                bot = instaloader.Instaloader()
                response = requests.get(web_data["url"])
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")   
                    
                    links = soup.find_all("a")
                    data = []
                    for link in links:
                        data.append(link.get("href"))
                    return JsonResponse({"data": data}, status=status.HTTP_200_OK) 
            else:
                return JsonResponse({"error_web_scrapping": "Website not reachable due to wrong website typed valid with http: or https"}, status=status.HTTP_204_NO_CONTENT) 
        return JsonResponse({"error_scrapping": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 

    @api_view(['GET', "DELETE"])
    def api_scrapping_history_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        if request.method == 'GET':
            try:
                auth_get = Authentication.objects.filter(id=id_client).values()
                history = History.objects.filter(email=auth_get[0]["email"]).values()
                history_serializer = HistorySerializer(history, many=True)
                return JsonResponse(history_serializer.data, safe=False, status=status.HTTP_200_OK)

            except:
                return JsonResponse({"data": ""}, status=status.HTTP_204_NO_CONTENT)

        if request.method == 'DELETE':
            
            try:
                auth_delete = History.objects.filter(email=user_client.email).delete()
                return JsonResponse({"result": True}, status=status.HTTP_200_OK) 

            except:
                return JsonResponse({"error_scrapping": "Something went wrong with id of user"}, status=status.HTTP_204_NO_CONTENT)

        return JsonResponse({"error_scrapping": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 


   
    

