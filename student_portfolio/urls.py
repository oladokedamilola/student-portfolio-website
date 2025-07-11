from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('auth/', include('accounts.urls')),
    path('p/', include('portfolio.urls')),
    path('c/', include('chat.urls')),

    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('students/dashboard/', views.student_dashboard, name='student_dashboard'),

     path('student/edit-profile/', views.edit_student_profile, name='edit_student_profile'),
    path('client/edit-profile/', views.edit_client_profile, name='edit_client_profile'),

    path('student/notifications/', views.student_notifications, name='student_notifications'),
    path('client/notifications/', views.client_notifications, name='client_notifications'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/mark-read/<int:notif_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/delete/<int:notif_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/fetch-next/', views.fetch_next_notification, name='fetch_next_notification'),



    path('favorites/', views.favorite_students_list, name='favorite_students_list'),

    path('search/', views.public_search, name='public_search'),

    path('student/<str:matric_number>/portfolio/', views.public_portfolio, name='public_portfolio'),

    path('favorite/add/<str:matric_number>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<str:matric_number>/', views.remove_favorite, name='remove_favorite'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)