from django.urls import path, include

from .views import *

urlpatterns = [
    path(r'', posts_list, name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('sign-up/', UserCreate.as_view(), name='user_sign_up_url'),
    path('sign-in/', sign_in, name='user_sign_in_url'),
    path('user/<int:id>/', UserDetail.as_view(), name='user_detail_url'),
    path('users/', users_list, name='users_list_url'),
    path('logout/', logout_view, name='logout_url'),

]
