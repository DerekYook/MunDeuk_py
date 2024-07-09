from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserList

from .serializers import GroupSerializer, UserSerializer


# 클라이언트 요청 처리 및 비즈니스로직 수행 (Spring의 Controller와 유사한 느낌)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# API 뷰 추가
def index(request):
    return render(request, 'index.html')


class UserListView(APIView):
    def get(self, request):
        users = UserList.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
