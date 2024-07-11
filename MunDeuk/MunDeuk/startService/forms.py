from django import forms
from .models import MemberInfo


class MemberForm(forms.ModelForm):
    class Meta:
        model = MemberInfo
        fields = ['nickName', 'email', 'password', 'memberAuth', 'memberState']
