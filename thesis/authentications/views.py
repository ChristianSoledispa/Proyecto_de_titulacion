

# from django.shortcuts import render
# from django.http import HttpResponse




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


from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from authentications.models import Authentication
from authentications.serializers import AuthenticationSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
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
def authentication_list_is_superuser(request):
    auths = Authentication.objects.filter(is_superuser=True)
        
    if request.method == 'GET': 
        auths_serializer = AuthenticationSerializer(auths, many=True)
        return JsonResponse(auths_serializer.data, safe=False)
    
