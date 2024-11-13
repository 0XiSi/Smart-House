from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Relay, DH11

class RelaySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Relay
        fields = '__all__'


class DH11Serializer(serializers.ModelSerializer):
    class Meta:
        model = DH11
        fields = '__all__'
