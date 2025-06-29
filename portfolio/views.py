from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import StudentProfile
from django.contrib.auth.decorators import login_required
from portfolio.models import Project, Research, Internship
from .forms import *
from django.contrib import messages     
from django.db.models import Q


@login_required
def add_project(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = profile
            project.save()
            messages.success(request, "Project added successfully.")
            return redirect('student_dashboard')
    else:
        form = ProjectForm()
    return render(request, 'portfolio/forms/project_form.html', {'form': form})


@login_required
def edit_project(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, pk=pk, student=profile)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect('student_dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'portfolio/forms/project_form.html', {'form': form})


@login_required
def delete_project(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, pk=pk, student=profile)
    project.delete()
    messages.success(request, "Project deleted.")
    return redirect('student_dashboard')


@login_required
def add_research(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            research = form.save(commit=False)
            research.student = profile
            research.save()
            messages.success(request, "Research added.")
            return redirect('student_dashboard')
    else:
        form = ResearchForm()
    return render(request, 'portfolio/forms/research_form.html', {'form': form})


@login_required
def edit_research(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    research = get_object_or_404(Research, pk=pk, student=profile)

    if request.method == "POST":
        form = ResearchForm(request.POST, request.FILES, instance=research)
        if form.is_valid():
            form.save()
            messages.success(request, "Research updated.")
            return redirect('student_dashboard')
    else:
        form = ResearchForm(instance=research)
    return render(request, 'portfolio/forms/research_form.html', {'form': form})


@login_required
def delete_research(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    research = get_object_or_404(Research, pk=pk, student=profile)
    research.delete()
    messages.success(request, "Research deleted.")
    return redirect('student_dashboard')


@login_required
def add_internship(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.student = profile
            internship.save()
            messages.success(request, "Internship added.")
            return redirect('student_dashboard')
    else:
        form = InternshipForm()
    return render(request, 'portfolio/forms/internship_form.html', {'form': form})


@login_required
def edit_internship(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    internship = get_object_or_404(Internship, pk=pk, student=profile)

    if request.method == "POST":
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, "Internship updated.")
            return redirect('student_dashboard')
    else:
        form = InternshipForm(instance=internship)
    return render(request, 'portfolio/forms/internship_form.html', {'form': form})


@login_required
def delete_internship(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    internship = get_object_or_404(Internship, pk=pk, student=profile)
    internship.delete()
    messages.success(request, "Internship deleted.")
    return redirect('student_dashboard')






@login_required

@login_required
def add_favorite(request, matric_number):
    student_profile = get_object_or_404(StudentProfile, matric_number=matric_number)
    user = request.user

    Favorite.objects.get_or_create(user=user, student=student_profile)

    # Create notification
    Notification.objects.create(
        student=student_profile,
        message=f"{user.email} starred your portfolio."
    )

    messages.success(request, f"Added {student_profile.first_name} to favorites.")
    return redirect('public_portfolio', matric_number=matric_number)


@login_required
def remove_favorite(request, matric_number):
    if request.user.role != 'CLIENT':
        messages.error(request, "Only clients can remove favorites.")
        return redirect('login')

    client_profile = ClientProfile.objects.get(user=request.user)
    student_profile = get_object_or_404(StudentProfile, matric_number=matric_number)

    Favorite.objects.filter(client=client_profile, student=student_profile).delete()
    messages.success(request, f"Removed {student_profile.first_name} from favorites.")
    return redirect('public_portfolio', matric_number=matric_number)



