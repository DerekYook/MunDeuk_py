from urllib.request import Request

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .addon.JWTAuthentication import JWTAuthentication
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
    # if request.method == 'POST':
    #     serializer = MemberSerializer(data=request.data)
    #     print(request)
    #     print(serializer)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)
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
@csrf_exempt
@api_view(['GET'])
def member_login(request):
    return render(request, 'login.html')


# @swagger_auto_schema(
#     method='post',
#     request_body=MemberSerializer,
#     responses={
#         200: openapi.Response('Ok', MemberSerializer),
#         400: 'Bad Request',
#         401: 'Unauthorized'
#     }
# )
# @api_view(['POST'])
# def member_login_ajax(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#
#         if serializer.is_valid():
#             email = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')
#             try:
#                 # member = MemberInfo.objects.get(email=email, password=password)
#                 # # 사용자 인증에 성공하면 사용자 데이터를 반환합니다
#                 # return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)
#                 user = authenticate(request, email=email, password=password)
#                 print("+++123")
#                 if user is not None:
#                     token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')
#                     response = Response()
#                     response.set_cookie(
#                         key='jwt',
#                         value=token,
#                         httponly=True,
#                         secure=True,
#                         samesite='Strict',
#                         max_age=3600,
#                     )
#                     response.data = {'message': 'Login successful'}
#                     return response
#                 else:
#                     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#             except MemberInfo.DoesNotExist:
#                 # 사용자 인증에 실패하면 401 Unauthorized 응답을 반환합니다
#                 return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Render the memberList page",
    responses={
        200: openapi.Response('Members page rendered'),
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

        # 새로운 access 토큰이 요청 객체에 있는지 확인하고, 쿠키에 설정합니다.
        if hasattr(request, 'new_access_token'):
            response.set_cookie(key='access', value=request.new_access_token, httponly=True)

        if hasattr(request, 'new_refresh_token'):
            response.set_cookie(key='refresh', value=request.new_refresh_token, httponly=True)

        return response

    def get(self, request):
        response = Response({"detail": "new tokens"})
        print(request)

        # 새로운 access 토큰이 요청 객체에 있는지 확인하고, 쿠키에 설정합니다.
        if hasattr(request, 'new_access_token'):
            response.set_cookie(key='access', value=request.new_access_token, httponly=True)

        if hasattr(request, 'new_refresh_token'):
            response.set_cookie(key='refresh', value=request.new_refresh_token, httponly=True)

        return response