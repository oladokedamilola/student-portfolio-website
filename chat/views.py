from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatThread, Message
from accounts.models import StudentProfile, ClientProfile, User
from portfolio.models import Notification
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string


@login_required
def start_chat(request, matric_number):
    if request.user.role != 'CLIENT':
        messages.error(request, "Only clients can start chats.")
        return redirect('home')

    student_profile = get_object_or_404(StudentProfile, registry__matric_number=matric_number)
    client_profile = get_object_or_404(ClientProfile, user=request.user)

    # Check if chat already exists
    thread, created = ChatThread.objects.get_or_create(student=student_profile, client=client_profile)

    return redirect('chat_detail', thread_id=thread.id)

@login_required
def chat_inbox(request):
    if request.user.role == 'CLIENT':
        profile = get_object_or_404(ClientProfile, user=request.user)
        threads = ChatThread.objects.filter(client=profile).order_by('-created_at')
    elif request.user.role == 'STUDENT':
        profile = get_object_or_404(StudentProfile, user=request.user)
        threads = ChatThread.objects.filter(student=profile).order_by('-created_at')
    else:
        threads = []

    # Annotate each thread with last message
    for t in threads:
        last_msg = t.messages.order_by('-timestamp').first()
        t.last_message = last_msg

    return render(request, 'chat/inbox.html', {'threads': threads})


from django.http import JsonResponse

@login_required
def chat_detail(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id)

    # Check authorization
    if request.user.role == 'CLIENT' and thread.client.user != request.user:
        messages.error(request, "Unauthorized.")
        return redirect('chat_inbox')
    if request.user.role == 'STUDENT' and thread.student.user != request.user:
        messages.error(request, "Unauthorized.")
        return redirect('chat_inbox')

    # Mark all unread messages as read
    Message.objects.filter(thread=thread, is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            msg = Message.objects.create(thread=thread, sender=request.user, content=content)

            # Create notification
            if request.user.role == 'CLIENT':
                Notification.objects.create(
                    student=thread.student,
                    message=f"New message from {thread.client.first_name}: {content[:30]}..."
                )
            elif request.user.role == 'STUDENT':
                Notification.objects.create(
                    client=thread.client,
                    message=f"New message from {thread.student.registry.first_name}: {content[:30]}..."
                )

        messages_list = thread.messages.order_by('timestamp')

        # Always check if AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('chat/messages_partial.html', {
                'messages': messages_list,
                'user': request.user,
            }, request=request)
            return JsonResponse({'status': 'success', 'html': html})

        # If not AJAX fallback
        return redirect('chat_detail', thread_id=thread.id)

    messages_list = thread.messages.order_by('timestamp')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('chat/messages_partial.html', {
            'messages': messages_list,
            'user': request.user,
        }, request=request)
        return JsonResponse({'status': 'success', 'html': html})

    return render(request, 'chat/thread_detail.html', {
        'thread': thread,
        'messages': messages_list,
    })

