from django.urls import path
from . import views

urlpatterns = [

    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),
    
    path('research/add/', views.add_research, name='add_research'),
    path('research/edit/<int:pk>/', views.edit_research, name='edit_research'),
    path('research/delete/<int:pk>/', views.delete_research, name='delete_research'),

    path('internships/add/', views.add_internship, name='add_internship'),
    path('internships/edit/<int:pk>/', views.edit_internship, name='edit_internship'),
    path('internships/delete/<int:pk>/', views.delete_internship, name='delete_internship'),


    path('favorite/add/<str:matric_number>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<str:matric_number>/', views.remove_favorite, name='remove_favorite'),

]
