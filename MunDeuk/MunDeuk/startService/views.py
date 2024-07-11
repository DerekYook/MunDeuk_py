from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import MemberForm

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MemberInfo
from .serializers import MemberSerializer, VerifyMember
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


def index(request):
    return render(request, 'index.html')


@swagger_auto_schema(
    method='get',
    operation_description="Render the login page",
    responses={200: openapi.Response('Login page rendered')}
)
@csrf_exempt
@api_view(['GET'])
def member_signup(request):
    return render(request, 'signup.html')


@swagger_auto_schema(
    method='post',
    request_body=MemberSerializer,
    responses={
        201: openapi.Response('Created', MemberSerializer),
        400: 'Bad Request'
    }
)
@api_view(['POST'])
def member_signup_ajax(request):
    if request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@swagger_auto_schema(
    method='get',
    operation_description="Render the login page",
    responses={200: openapi.Response('Login page rendered')}
)
@csrf_exempt
@api_view(['GET'])
def member_login(request):
    return render(request, 'login.html')


@swagger_auto_schema(
    method='post',
    request_body=MemberSerializer,
    responses={
        200: openapi.Response('Ok', MemberSerializer),
        400: 'Bad Request',
        401: 'Unauthorized'
    }
)
@api_view(['POST'])
def member_login_ajax(request):
    if request.method == 'POST':
        serializer = VerifyMember(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                member = MemberInfo.objects.get(email=email, password=password)
                # 사용자 인증에 성공하면 사용자 데이터를 반환합니다
                return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)
            except MemberInfo.DoesNotExist:
                # 사용자 인증에 실패하면 401 Unauthorized 응답을 반환합니다
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
