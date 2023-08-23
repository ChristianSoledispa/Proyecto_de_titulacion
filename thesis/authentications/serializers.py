from rest_framework import serializers 
from authentications.models import Authentication, History
 
 
class AuthenticationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Authentication
        fields = ('id',
                  'username',
                  'email',
                  'password',
                  'is_superuser')
        

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'
