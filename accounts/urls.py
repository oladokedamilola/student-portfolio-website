from django.urls import path
from . import views

urlpatterns = [
    path('verify-matric/', views.verify_matric, name='verify_matric'),
    path('student/register/', views.student_register, name='student_register'),

    path('client/register/', views.client_register, name='client_register'),
    path('client/verify/', views.verify_nin, name='verify_nin'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
