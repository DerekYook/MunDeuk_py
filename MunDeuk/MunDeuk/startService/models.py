from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.
# class MemberInfo(models.Model):
#     class MemberAuth(models.TextChoices):
#         # Enum_val = 'db_val', 'display_val'
#         USER = 'USER', 'User'
#         ADMIN = 'ADMIN', 'Admin'
#
#     class MemberState(models.TextChoices):
#         ACTIVE = 'A', 'Active'
#         INACTIVE = 'I', 'Inactive'
#         BANNED = 'B', 'Banned'
#
#     nickName = models.CharField(max_length=100)
#     email = models.EmailField(default='default@example.com')
#     password = models.CharField(max_length=100)
#     memberAuth = models.CharField(max_length=100, choices=MemberAuth.choices, default=MemberAuth.USER)
#     memberState = models.CharField(max_length=1, choices=MemberState.choices, default=MemberState.ACTIVE)
#
#     def to_dic(self):
#         return {
#             "nickName": self.nickName,
#             "email": self.email,
#             "password": self.password,
#             "memberAuth": self.memberAuth,
#             "memberState": self.memberState
#         }
class MemberInfoManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일을 입력해야 합니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호를 해시화합니다.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class MemberInfo(AbstractBaseUser, PermissionsMixin):
    class MemberAuth(models.TextChoices):
        USER = 'USER', 'User'
        ADMIN = 'ADMIN', 'Admin'

    class MemberState(models.TextChoices):
        ACTIVE = 'A', 'Active'
        INACTIVE = 'I', 'Inactive'
        BANNED = 'B', 'Banned'

    nickName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    memberAuth = models.CharField(max_length=100, choices=MemberAuth.choices, default=MemberAuth.USER)
    memberState = models.CharField(max_length=1, choices=MemberState.choices, default=MemberState.ACTIVE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MemberInfoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def to_dic(self):
        return {
            "userId": self.id,
            "nickName": self.nickName,
            "email": self.email,
            "password": self.password,
            "memberAuth": self.memberAuth,
            "memberState": self.memberState
        }
