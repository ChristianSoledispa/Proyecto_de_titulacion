

from django.shortcuts import render
from django.http import HttpResponse




from rest_framework.views import APIView
from mongo_auth.permissions import AuthenticatedOnly
from rest_framework.response import Response
from rest_framework import status

from mongo_auth.permissions import AuthenticatedOnly
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class GetTest(APIView):

    permission_classes = [AuthenticatedOnly]

    def get(self, request, format=None):
        try:
            print(request.user)  # This is where magic happens
            return Response(status=status.HTTP_200_OK,
                            data={"data": {"msg": "User Authenticated"}})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
# @api_view(["GET"])
# @permission_classes([AuthenticatedOnly])   
def auths(request):
    print(request.user)
    print(request.method)
    return HttpResponse("Hello world!")
    try:
        print(request.user)
        return Response(status=status.HTTP_200_OK,
                        data={"data": {"msg": "User Authenticated"}})
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)