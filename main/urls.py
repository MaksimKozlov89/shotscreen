from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.register, name='register'),
    path('add/', views.add_screenshot, name='add'),
    path('account/<filter_>', views.account, name='account'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload/', views.upload, name='upload'),
    path('delete/<int:id_screen>', views.delete, name='delete'),
    path('<int:pk>', views.screen_detail, name='screen_detail'),
    path('download/', views.download, name='download'),
]
