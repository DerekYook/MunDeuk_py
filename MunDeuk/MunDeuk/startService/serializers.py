from django.contrib.auth.models import Group, User
from django.conf import settings
from rest_framework import serializers
from .models import MemberInfo


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        # # model 지정
        # model = MemberInfo
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'nickName', 'email', 'password']


class VerifyMember(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'email', 'password']


class MembersList(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'nickName', 'email', 'memberAuth', 'memberState']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

