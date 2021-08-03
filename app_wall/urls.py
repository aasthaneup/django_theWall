from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('post_msg', views.post_message),
    path('post_cmt/<int:id>', views.post_comment),
    path('delete/<int:id>', views.delete_post)

]