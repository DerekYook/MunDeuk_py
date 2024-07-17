from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from ..serializers import MembersList
from ..models import MemberInfo
import jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("JWTAuthentication authenticate called")  # 디버깅 로그 추가
        token = request.COOKIES.get('jwt')
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
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
            print(user)
        except UserModel.DoesNotExist:
            return None
        print("before chk passwd")
        print(user.password)
        print(password)
        if user.check_password(password):
            print(password)
            print(user)
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
