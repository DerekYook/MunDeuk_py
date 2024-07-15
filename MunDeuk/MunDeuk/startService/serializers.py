from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import MemberInfo


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberInfo
        fields = ['id', 'nickName', 'email', 'password']


class VerifyMember(serializers.ModelSerializer):
    class Meta:
        model = MemberInfo
        fields = ['id', 'email', 'password']


class MembersList(serializers.ModelSerializer):
    class Meta:
        model = MemberInfo
        fields = ['id', 'nickName', 'email', 'memberAuth', 'memberState']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

