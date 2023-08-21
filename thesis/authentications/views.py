
from django.shortcuts import render


from rest_framework.views import APIView


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from authentications.models import Authentication
from authentications.serializers import AuthenticationSerializer
from rest_framework.decorators import api_view



from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.forms.models import model_to_dict

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
 
import datetime
from django.template import loader
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import pyotp
from django.contrib.auth.models import User
from django.urls import reverse       
import pymongo
from django.http import HttpResponseRedirect
from django.urls import reverse
import instaloader
from django.core import serializers
import requests
from bs4 import BeautifulSoup


connect_string ='mongodb+srv://heroe:heroe@cluster0.wkxtx.mongodb.net/1christthesis?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['1christthesis']
collection_name = dbname["authentications_authentication"]

class ScrappingAPI(APIView):



    def login_view(request):

        # error_message = None
        # my_client = pymongo.MongoClient(connect_string)
        # dbname = my_client['1christthesis']
        # collection_name = dbname["authentications_authentication"]

        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            print("username: %s" % username, "password: %s" % password)
            # login_details = list(collection_name.find({
            #     "username":f"{username}"}))
            # login_details = list(collection_name.find({"username":username}))
            # print("login_details: %s" % login_details, "password: %s" % password)

            
            login_details = Authentication.objects.filter(email=username).values().first()
            print("login_details: %s" % login_details, "password: %s" % password)
            if login_details is not None:
                # details_client = login_details.pop()
                # print("details_client", details_client)
                # return HttpResponseRedirect(reverse('scrapping', args=(list({'id_client': login_details}))))
                return redirect('scrapping',id_client=1)

        return render(request, "login.html", {'error_message': 'Invalid username or password'})

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


    def scrapping_user_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        print("user_client: %s" % user_client.username)
        context ={ 'user': user_client}
        if request.method == 'POST':
            user_typed = request.POST.get('user_typed')
            if user_typed: 
                bot = instaloader.Instaloader()
                
                cuenta=user_typed
                profile_crapp = instaloader.Profile.from_username(bot.context, cuenta)
                context["profile_crapp"] = profile_crapp
            else:
                context["error_scrapping"] = "Unknown User"
        return render(request, "scrapping.html", context)

    def scrapping_web_view(request, id_client):
        # print("id_client: ", request["id_client"])
        user_client = Authentication.objects.get(id=id_client)
        template = loader.get_template('scrapping.html')

        context={ "user": user_client}
        if request.method == 'POST':
            web_typed = request.POST.get('web_typed')
            another = request.POST.get('loco_typed')
            
            if web_typed: 

                # if web_typed.startswith('www.'):
                    
                # url = "https://www.lamborghini.com/en-en"
                url = web_typed
                print("url", url)
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    links = soup.find_all("a")
                    data = []
                    for link in links:
                        data.append(link.get("href"))
                        # print(link.get("href"))

                    context["website_scrapping"] = data
                    # request["id_client"] = id_client
                    # return render(request, template,  context, id_client=id_client)
                    return render(request, "scrapping.html",  context)
                else:
                    context["error_scrapping"] = f"Website not reachable due to wrong website typed {web_typed}"
            else:
                context["error_scrapping"] = "Required email correctly of the website"
        return redirect("scrapping.html", id_client=id_client)
    
    @api_view(['GET', 'POST'])
    def api_scrapping_user_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        print("user_client: %s" % user_client.username)
        context ={ 'user': user_client}
        if request.method == 'POST':
            auth_data = JSONParser().parse(request)
            print("auth_data: ", auth_data)
            # user_typed = request.POST.get('user_typed')
            # print("user_typed:", user_typed)
            if auth_data: 
                print("succeeded")
                bot = instaloader.Instaloader()
                print("succeeded")
                cuenta="ronaldo"
                profile_crapp = instaloader.Profile.from_username(bot.context, cuenta)
                print("Username: ", profile_crapp.username)
                print("User ID: ", profile_crapp.userid)  
                print("Number of Posts: ", profile_crapp.mediacount   )
                print("Followers Count: ", profile_crapp.followers)   
                print("Following Count: ", profile_crapp.followees)   
                print("Bio: ", profile_crapp.biography)   
                print("External URL: ", profile_crapp.external_url)
                print(dir(profile_crapp))   
                l = [profile_crapp]
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


    @api_view(['GET', 'POST'])
    def api_scrapping_website_view(request, id_client):
        user_client = Authentication.objects.get(id=id_client)
        context ={ 'user': user_client}
        if request.method == 'POST':
            auth_data = JSONParser().parse(request)

            if auth_data: 
                bot = instaloader.Instaloader()
                response = requests.get(auth_data["url"])
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    links = soup.find_all("a")
                    data = []
                    for link in links:
                        data.append(link.get("href"))
                    return JsonResponse({"data": data}, status=status.HTTP_200_OK) 
            else:
                return JsonResponse({"error_scrapping": "Unknown User"}, status=status.HTTP_204_NO_CONTENT) 
        return JsonResponse({"error_scrapping": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 


    # def scrapping_web_view(request, id_client):
    #     user_client = Authentication.objects.get(id=id_client)
    #     context ={ 'user': user_client}
    #     if request.method == 'POST':
    #         web_typed = request.POST.get('web_typed')
    #         if web_typed: 
    #             # Send an HTTP GET request to the URL
    #             url = "https://www.lamborghini.com/en-en"
    #             response = requests.get(url)
                
    #             # Check if the request was successful
    #             if response.status_code == 200:
    #                 # Parse the HTML content using BeautifulSoup
    #                 soup = BeautifulSoup(response.content, "html.parser")
                    
    #                 # Find and print specific elements from the page
    #                 # Example: Extract and print all the links
    #                 links = soup.find_all("a")
    #                 print(soup, "Successfully parsed1")
    #                 print(type(soup), len(soup))
    #                 print(soup, "Successfully parsed")
    #                 # for link in links:
    #                 #     print(link.get("href"))

    #                 context["web_scrapping"] = links
    #                 return render(request, "scrapping.html", context)
    #             else:
    #                 context["error_web"] = f"Nothing to display here. {url}"
    #         else:
    #             context["error_web"] = "Error in your web address"
    #     return render(request, "scrapping.html", context)
    

# from rest_framework.views import APIView
# from mongo_auth.permissions import AuthenticatedOnly
# from rest_framework.response import Response
# from rest_framework import status

# from mongo_auth.permissions import AuthenticatedOnly
# from rest_framework.decorators import permission_classes
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# class GetTest(APIView):

#     permission_classes = [AuthenticatedOnly]

#     def get(self, request, format=None):
#         try:
#             print(request.user)  # This is where magic happens
#             return Response(status=status.HTTP_200_OK,
#                             data={"data": {"msg": "User Authenticated"}})
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
        
# # @api_view(["GET"])
# # @permission_classes([AuthenticatedOnly])   
# def auths(request):
#     print(request.user)
#     print(request.method)
#     return HttpResponse("Hello world!")
#     try:
#         print(request.user)
#         return Response(status=status.HTTP_200_OK,
#                         data={"data": {"msg": "User Authenticated"}})
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)

