from django.urls import path
from . import views

urlpatterns = [
    path('chat/start/<str:matric_number>/', views.start_chat, name='start_chat'),
    path('chat/inbox/', views.chat_inbox, name='chat_inbox'),
    path('chat/<int:thread_id>/', views.chat_detail, name='chat_detail'),
]
