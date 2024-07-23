import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from ..serializers import MembersList
from ..models import MemberInfo
import jwt, datetime


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("JWTAuthentication authenticate called")  # 디버깅 로그 추가
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')

        if not access_token and not refresh_token:
            return None

        try:
            # access토큰 유효성 검증
            if access_token:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                user = MemberInfo.objects.get(id=payload['user_id'])
                return (user, None)
            # elif refresh_token:
            #     payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            #     user = MemberInfo.objects.get(id=payload['user_id'])
            #     new_access_token = jwt.encode(
            #         {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
            #         settings.SECRET_KEY, algorithm='HS256')
            #     # response = request.response
            #     response = HttpResponse()
            #     response.set_cookie(key='access', value=new_access_token, httponly=True)
            #     return (user, None)
        except jwt.ExpiredSignatureError:
            # access토큰 만료기간 확인 및 refresh토큰 유효성 확인
            if refresh_token:
                try:
                    print("refresh_token_reissuance")
                    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = MemberInfo.objects.get(id=payload['user_id'])
                    new_access_token = jwt.encode(
                        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)},
                        settings.SECRET_KEY, algorithm='HS256')
                    print(new_access_token)
                    # # response = request.response
                    # response = HttpResponse()
                    # response.set_cookie(key='access', value=new_access_token, httponly=True)

                    new_refresh_token = jwt.encode(
                        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)},
                        settings.SECRET_KEY, algorithm='HS256')
                    print(new_refresh_token)
                    request.new_access_token = new_access_token
                    request.new_refresh_token = new_refresh_token
                    print(request)
                    return (user, None)
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Refresh token has expired')
                except jwt.InvalidTokenError:
                    raise AuthenticationFailed('Invalid refresh token')
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            user = MemberInfo.objects.get(id=payload['user_id'])
        except MemberInfo.DoesNotExist:
            raise AuthenticationFailed('User not found')
        return (user, None)


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("EmailBackend authenticate called")  # 디버깅 로그 추가
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
