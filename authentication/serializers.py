from rest_framework import serializers
from authentication.models import UsersTab


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTab
        fields = '__all__'
