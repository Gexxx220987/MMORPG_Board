from django.urls import path

from .views import SignUp, SignUpCheckEmail, UserLogin, UserLogout

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup_check_email/<int:pk>/', SignUpCheckEmail.as_view(), name='signup_check_email'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout')
]
