from django.db import models


# Create your models here.
class MemberInfo(models.Model):
    class MemberAuth(models.TextChoices):
        # Enum_val = 'db_val', 'display_val'
        USER = 'USER', 'User'
        ADMIN = 'ADMIN', 'Admin'

    class MemberState(models.TextChoices):
        ACTIVE = 'A', 'Active'
        INACTIVE = 'I', 'Inactive'
        BANNED = 'B', 'Banned'

    nickName = models.CharField(max_length=100)
    email = models.EmailField(default='default@example.com')
    password = models.CharField(max_length=100)
    memberAuth = models.CharField(max_length=100, choices=MemberAuth.choices, default=MemberAuth.USER)
    memberState = models.CharField(max_length=1, choices=MemberState.choices, default=MemberState.ACTIVE)

    def to_dic(self):
        return {
            "nickName": self.nickName,
            "email": self.email,
            "password": self.password,
            "memberAuth": self.memberAuth,
            "memberState": self.memberState
        }

