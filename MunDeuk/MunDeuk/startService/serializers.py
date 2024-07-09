from django.contrib.auth.models import Group, User
from rest_framework import serializers


# 데이터 표현 (Spring의 DTO와 유사한 느낌)
# => 쿼리셋, 모델 인스턴스와 같은 복잡한 데이터를 JSON, XML과 같이 간단한 데이터로 변환하는 것이라고 한다.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SearchUser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']
