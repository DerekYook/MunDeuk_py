from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import MemberForm

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MemberInfo
from .serializers import MemberSerializer, VerifyMember, MembersList
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


def index(request):
    return render(request, 'index.html')


@swagger_auto_schema(
    method='get',
    operation_description="Render the signup page",
    responses={
        200: openapi.Response('Signup page rendered'),
        404: 'Not Found'
    }
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
    responses={
        200: openapi.Response('Login page rendered'),
        404: 'Not Found'
    }
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


@swagger_auto_schema(
    method='get',
    operation_description="Render the memberList page",
    responses={
        200: openapi.Response('Login page rendered'),
        404: 'Not Found'
    }
)
@csrf_exempt
@api_view(['GET'])
def members_list(request):
    if request.method == 'GET':
        members = MemberInfo.objects.all()
        serializer = MembersList(members, many=True)
    return render(request, 'admin.html', {'members': serializer.data})


@csrf_exempt
@api_view(['POST'])
def members_update(request):
    if request.method == 'POST':
        for member_data in request.data:
        #     member = MemberInfo.objects.get(id=member_data['id'])
        #     member.memberAuth = member_data['memberAuth']
        #     member.memberState = member_data['memberState']
        #     member.save()
        # return Response(status=status.HTTP_200_OK)
            try:
                member = MemberInfo.objects.get(id=member_data['id'])
                member.memberAuth = member_data['memberAuth']
                member.memberState = member_data['memberState']
                member.save()
            except MemberInfo.DoesNotExist:
                return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": "Members updated successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
