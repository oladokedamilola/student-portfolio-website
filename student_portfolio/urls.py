from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('auth/', include('accounts.urls')),
    path('p/', include('portfolio.urls')),

    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('students/dashboard/', views.student_dashboard, name='student_dashboard'),

     path('student/edit-profile/', views.edit_student_profile, name='edit_student_profile'),
    path('client/edit-profile/', views.edit_client_profile, name='edit_client_profile'),

    path('student/notifications/', views.student_notifications, name='student_notifications'),

    path('search/', views.public_search, name='public_search'),

    path('student/<str:matric_number>/portfolio/', views.public_portfolio, name='public_portfolio'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)