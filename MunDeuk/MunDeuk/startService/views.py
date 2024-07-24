from tokenize import TokenError
from urllib.request import Request

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import MemberInfo
from .serializers import MemberSerializer, VerifyMember, MembersList, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# import jwt
import json


# Create your views here.

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
        try:
            data = json.loads(request.body)
            User = get_user_model()

            # 이메일 중복 확인
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': '이미 존재하는 이메일입니다.'}, status=400)

            # 사용자 생성
            user = User.objects.create(
                nickName=data['nickName'],
                email=data['email'],
                password=make_password(data['password']),  # 비밀번호 해시화
                # memberAuth=data['memberAuth'],  # 필요한 경우 추가 필드
                # memberState=data['memberState'],  # 필요한 경우 추가 필드
            )
            return JsonResponse({'message': '회원가입 성공'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=400)


@swagger_auto_schema(
    method='get',
    operation_description="Render the login page",
    responses={
        200: openapi.Response('Login page rendered'),
        404: 'Not Found'
    }
)
@api_view(['GET'])
def member_login(request):
    return render(request, 'login.html')


@swagger_auto_schema(
    method='get',
    operation_description="Render the memberList page",
    responses={
        200: openapi.Response('Members page rendered'),
        404: 'Not Found'
    }
)
@api_view(['GET'])
def members_list(request):
    if request.method == 'GET':
        members = MemberInfo.objects.all()
        serializer = MembersList(members, many=True)
    return render(request, 'admin.html', {'members': serializer.data})


@api_view(['POST'])
def members_update(request):
    if request.method == 'POST':
        for member_data in request.data:
            try:
                member = MemberInfo.objects.get(id=member_data['id'])
                member.memberAuth = member_data['memberAuth']
                member.memberState = member_data['memberState']
                member.save()
            except MemberInfo.DoesNotExist:
                return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": "Members updated successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    # TokenObtainPairView 의 response 는 refresh, access 토큰 정보를 반환하기 때문에
    # "login success" 로 바꾸고 토큰은 쿠키에 담아서 응답.
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)

        response = Response({"detail": "login success"}, status=status.HTTP_200_OK)
        response.set_cookie("refresh", res.data.get('refresh', None), httponly=True)
        response.set_cookie("access", res.data.get('access', None), httponly=True)

        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        response.data['access_token'] = access_token
        response.data['refresh_token'] = refresh_token

        return response


class InvalidToken:
    pass


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh', '토큰이 업서용')
        data = {"refresh": refresh_token}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token = serializer.validated_data
        response = Response({"detail": "refresh success"}, status=status.HTTP_200_OK)
        response.set_cookie("refresh", token['refresh'], httponly=True)
        response.set_cookie("access", token['access'], httponly=True)

        return response


class LogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh', '토큰이 업서용')
        data = {"refresh": str(refresh_token)}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response({"detail": "token blacklisted"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        response.delete_cookie("access")

        return response
