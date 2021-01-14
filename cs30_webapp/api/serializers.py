from rest_framework import serializers
from api.models import FlatfileEntry

class ApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatfileEntry
        fields = ('id','title')