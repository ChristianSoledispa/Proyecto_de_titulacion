from rest_framework import serializers 
from authentications.models import Authentication
 
 
class AuthenticationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Authentication
        fields = ('id',
                  'username',
                  'email',
                  'password',
                  'is_superuser')
