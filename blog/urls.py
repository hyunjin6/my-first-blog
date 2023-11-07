from django.urls import path 
from . import views
from django.urls import include
from django.contrib.auth.models import User
from rest_framework import routers


router = routers.DefaultRouter()
router.register('Post', views.IntruderImage)


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api_root/', include(router.urls)),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_root/Post/', views.post_data, name='post_data'),
]

