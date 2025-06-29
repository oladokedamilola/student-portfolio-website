from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import *
from portfolio.models import *
from django.contrib import messages
from django.db.models import Q
from portfolio.forms import *
from accounts.forms import *


def home(request):
    return render(request, 'home.html')

def public_search(request):
    query = request.GET.get('q', '')

    results = []
    if query:
        results = StudentProfile.objects.filter(
            Q(registry__first_name__icontains=query) |
            Q(registry__last_name__icontains=query) |
            Q(registry__department__icontains=query) |
            Q(registry__faculty__icontains=query)
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
        'internships': internships
    })


@login_required
def student_notifications(request):
    profile = StudentProfile.objects.get(user=request.user)
    notifications = profile.notifications.all().order_by('-created_at')

    return render(request, 'portfolio/students/student_notifications.html', {
        'notifications': notifications
    })


def client_dashboard(request):
    if request.user.role != 'CLIENT':
        messages.error(request, "Access denied. Only clients can view this page.")
        return redirect('login')

    profile = ClientProfile.objects.get(user=request.user)

    # Optional: show recent or suggested students
    recent_students = StudentProfile.objects.all().order_by('-id')[:10]

    return render(request, 'portfolio/clients/client_dashboard.html', {
        'profile': profile,
        'recent_students': recent_students
    })



@login_required
def edit_student_profile(request):
    if request.user.role != 'STUDENT':
        messages.error(request, "Only students can edit their profile.")
        return redirect('login')

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
        messages.error(request, "Only clients can edit profile.")
        return redirect('login')

    profile = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ClientProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('client_dashboard')
    else:
        form = ClientProfileEditForm(instance=profile)

    return render(request, 'portfolio/clients/edit_client_profile.html', {'form': form})



@login_required
def public_portfolio(request, matric_number):
    student_profile = get_object_or_404(StudentProfile, matric_number=matric_number)

    if request.user.role not in ["CLIENT", "STUDENT"]:
        messages.error(request, "Only authenticated users can view portfolios.")
        return redirect('login')

    if request.user != student_profile.user:
        Notification.objects.create(
            student=student_profile,
            message=f"{request.user.email} viewed your portfolio."
        )

    projects = student_profile.projects.all()
    research = student_profile.researches.all()
    internships = student_profile.internships.all()

    return render(request, 'portfolio/public_portfolio.html', {
        'student': student_profile,
        'projects': projects,
        'research': research,
        'internships': internships
    })