from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import *
from portfolio.models import *
from django.contrib import messages
from django.db.models import Q
from portfolio.forms import *
from accounts.forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def public_search(request):
    query = request.GET.get('q', '')

    results = StudentProfile.objects.none()  # Default empty queryset

    if query:
        results = StudentProfile.objects.filter(
            Q(header__icontains=query) |
            Q(projects__skills__name__icontains=query) |
            Q(researches__skills__name__icontains=query) |
            Q(internships__skills__name__icontains=query)
        ).distinct()

    return render(request, 'portfolio/public_search.html', {
        'query': query,
        'results': results
    })

@login_required
def student_dashboard(request):
    profile = StudentProfile.objects.get(user=request.user)

    projects = Project.objects.filter(student=profile)
    research = Research.objects.filter(student=profile)
    internships = Internship.objects.filter(student=profile)

    return render(request, 'portfolio/students/dashboard.html', {
        'profile': profile,
        'projects': projects,
        'research': research,
        'internships': internships,
        'user': request.user
    })


from django.core.paginator import Paginator

@login_required
def student_notifications(request):
    profile = StudentProfile.objects.get(user=request.user)
    notif_list = profile.notifications.all().order_by('-created_at')
    if request.GET.get('unread'):
        notif_list = notif_list.filter(is_read=False)

    # Use notif_list here before paginator
    unread_count = notif_list.filter(is_read=False).count()

    paginator = Paginator(notif_list, 5)
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)

    return render(request, 'portfolio/students/student_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })

@login_required
def client_notifications(request):
    profile = ClientProfile.objects.get(user=request.user)
    notif_list = profile.notifications.all().order_by('-created_at')
    
    if request.GET.get('unread'):
        notif_list = notif_list.filter(is_read=False)

    unread_count = notif_list.filter(is_read=False).count()

    paginator = Paginator(notif_list, 5)
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)

    return render(request, 'portfolio/clients/client_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def mark_all_notifications_read(request):
    if request.user.role == "STUDENT":
        profile = StudentProfile.objects.get(user=request.user)
        profile.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
        return redirect('student_notifications')

    elif request.user.role == "CLIENT":
        profile = ClientProfile.objects.get(user=request.user)
        profile.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
        return redirect('client_notifications')


from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)

    # Check ownership
    if request.user.role == "STUDENT" and notif.student and notif.student.user == request.user:
        notif.is_read = True
        notif.save()
    elif request.user.role == "CLIENT" and notif.client and notif.client.user == request.user:
        notif.is_read = True
        notif.save()
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"status": "unauthorized"}, status=403)
        messages.error(request, "Unauthorized.")
        return redirect('client_notifications' if request.user.role == "CLIENT" else 'student_notifications')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"status": "success"})

    messages.success(request, "Notification marked as read.")
    return redirect('client_notifications' if request.user.role == "CLIENT" else 'student_notifications')


@login_required
def delete_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)

    if (notif.student and notif.student.user == request.user) or (notif.client and notif.client.user == request.user):
        notif.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "deleted"})
        messages.success(request, "Notification deleted.")
    else:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "unauthorized"}, status=403)
        messages.error(request, "Unauthorized.")

    return redirect('client_notifications' if request.user.role == "CLIENT" else 'student_notifications')

from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def fetch_next_notification(request):
    user = request.user

    # Check role and profile
    if user.role == "STUDENT":
        profile = StudentProfile.objects.get(user=user)
        notifications_qs = profile.notifications.all().order_by('-created_at')
    elif user.role == "CLIENT":
        profile = ClientProfile.objects.get(user=user)
        notifications_qs = profile.notifications.all().order_by('-created_at')
    else:
        return JsonResponse({"status": "error", "message": "Invalid role"})

    # Get current page and per_page from request
    current_page = int(request.GET.get("current_page", 1))
    per_page = int(request.GET.get("per_page", 5))

    # Compute next offset
    total_notifications = notifications_qs.count()
    already_loaded = (current_page - 1) * per_page

    if already_loaded + per_page < total_notifications:
        next_notification = notifications_qs[already_loaded + per_page:already_loaded + per_page + 1].first()
    else:
        next_notification = None

    if next_notification:
        html = render_to_string("portfolio/partials/notification_item.html", {"note": next_notification}, request=request)
        return JsonResponse({"status": "success", "html": html})
    else:
        return JsonResponse({"status": "empty"})



def client_dashboard(request):
    if request.user.role != 'CLIENT':
        messages.error(request, "Access denied. Only clients can view this page.")
        return redirect('login')

    profile = ClientProfile.objects.get(user=request.user)

    favorites_qs = Favorite.objects.filter(
        user=request.user,
        student__registry__isnull=False,
        student__registry__matric_number__isnull=False
    ).select_related("student__registry").order_by("student__registry__last_name")

    recent_students = StudentProfile.objects.all().order_by('-id')[:10]

    return render(request, 'portfolio/clients/client_dashboard.html', {
        'profile': profile,
        'favorites': favorites_qs,
        'recent_students': recent_students,
        'user': request.user
    })




@login_required
def edit_student_profile(request):
    if request.user.role != 'STUDENT':
        messages.error(request, "Only students can edit their profile!")
        return redirect('home')

    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = StudentProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('student_dashboard')
    else:
        form = StudentProfileEditForm(instance=profile)

    return render(request, 'portfolio/students/edit_student_profile.html', {'form': form})

@login_required
def edit_client_profile(request):
    if request.user.role != 'CLIENT':
        messages.error(request, "Only clients can edit their profile!")
        return redirect('home')

    profile = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ClientProfileEditForm(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('client_dashboard')
    else:
        form = ClientProfileEditForm(instance=profile)

    return render(request, 'portfolio/clients/edit_client_profile.html', {'form': form})




@login_required
def public_portfolio(request, matric_number):
    student_profile = get_object_or_404(StudentProfile, registry__matric_number=matric_number)

    projects = student_profile.projects.all()
    research = student_profile.researches.all()
    internships = student_profile.internships.all()

    if request.user != student_profile.user:
        Notification.objects.create(
            student=student_profile,
            message=f"{request.user.email} viewed your portfolio."
        )

    is_favorited = False
    if request.user.is_authenticated and request.user.role == "CLIENT":
        is_favorited = Favorite.objects.filter(user=request.user, student=student_profile).exists()

    return render(request, 'portfolio/public_portfolio.html', {
        'student': student_profile,
        'projects': projects,
        'research': research,
        'internships': internships,
        'is_favorited': is_favorited,
    })



@login_required
def add_favorite(request, matric_number):
    student_profile = get_object_or_404(StudentProfile, registry__matric_number=matric_number)
    user = request.user

    Favorite.objects.get_or_create(user=user, student=student_profile)

    # Create notification
    Notification.objects.create(
        student=student_profile,
        message=f"{user.email} starred your portfolio."
    )

    messages.success(request, f"Added {student_profile.registry.first_name} to favorites.")
    return redirect('public_portfolio', matric_number=matric_number)


@login_required
def remove_favorite(request, matric_number):
    if request.user.role != 'CLIENT':
        messages.error(request, "Only clients can remove favorites.")
        return redirect('login')

    student_profile = get_object_or_404(StudentProfile, registry__matric_number=matric_number)
    Favorite.objects.filter(user=request.user, student=student_profile).delete()
    messages.success(request, f"Removed {student_profile.registry.first_name} from favorites.")
    return redirect('public_portfolio', matric_number=matric_number)



@login_required
def favorite_students_list(request):
    if request.user.role != "CLIENT":
        return redirect('home')

    favorites_qs = Favorite.objects.filter(
        user=request.user,
        student__registry__isnull=False,
        student__registry__matric_number__isnull=False
    ).select_related("student__registry").order_by("student__registry__last_name")

    paginator = Paginator(favorites_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'portfolio/clients/favorite_students_list.html', {
        'page_obj': page_obj,
    })

