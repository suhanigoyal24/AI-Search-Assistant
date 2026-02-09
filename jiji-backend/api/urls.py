from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Auth endpoints
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # API endpoint
    path('ask-jiji/', views.ask_jiji, name='ask_jiji'),
]
