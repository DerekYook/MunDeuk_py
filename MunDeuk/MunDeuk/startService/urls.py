from django.urls import path
# from .views import index, signup, UserListView, food_list # class가져오기
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', member_login, name='login'),
    path('member/login/', member_login_ajax, name='login-ajax'),
    path('signup/', member_signup, name='signup'),
    path('members/signup/', member_signup_ajax, name='signup-ajax'),
    path('members/list/', members_list, name='members-list'),
    path('members/update/', members_update, name='members-update')
]
