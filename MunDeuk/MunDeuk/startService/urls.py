from django.urls import path
from .views import index, UserListView # class가져오기

urlpatterns = [
    path('', index, name='index'),
    path('api/users/', UserListView.as_view(), name='user-list'),
]
