from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from portfolio.models import Project, Research, Internship
from .forms import *
from django.contrib import messages     
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from accounts.models import StudentProfile

from django.core import serializers
from django.http import JsonResponse
from .models import Skill


@login_required
def project_list(request):
    profile = StudentProfile.objects.get(user=request.user)
    project_list = Project.objects.filter(student=profile).order_by('-created_at')  # optional: newest first
    paginator = Paginator(project_list, 5)

    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(request, 'portfolio/project_list.html', {'projects': projects})


@login_required
def research_list(request):
    profile = StudentProfile.objects.get(user=request.user)
    research_list = Research.objects.filter(student=profile).order_by('-created_at')
    paginator = Paginator(research_list, 5)

    page_number = request.GET.get('page')
    researches = paginator.get_page(page_number)
    return render(request, 'portfolio/research_list.html', {'researches': researches})

@login_required
def internship_list(request):
    profile = StudentProfile.objects.get(user=request.user)
    internship_list = Internship.objects.filter(student=profile).order_by('-created_at')
    paginator = Paginator(internship_list, 5)

    page_number = request.GET.get('page')
    internships = paginator.get_page(page_number)
    return render(request, 'portfolio/internship_list.html', {'internships': internships})



def project_detail(request, pk, matric_number):
    student_registry = get_object_or_404(StudentRegistry, matric_number=matric_number)
    student_profile = get_object_or_404(StudentProfile, registry=student_registry)
    project = get_object_or_404(Project, pk=pk, student=student_profile)

    is_owner = False
    if request.user.is_authenticated and hasattr(request.user, "studentprofile"):
        if request.user.studentprofile == student_profile:
            is_owner = True

    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'student': student_profile,
        'is_owner': is_owner,
    })

def research_detail(request, pk, matric_number):
    student_registry = get_object_or_404(StudentRegistry, matric_number=matric_number)
    student_profile = get_object_or_404(StudentProfile, registry=student_registry)
    research = get_object_or_404(Research, pk=pk, student=student_profile)

    is_owner = False
    if request.user.is_authenticated and hasattr(request.user, "studentprofile"):
        if request.user.studentprofile == student_profile:
            is_owner = True

    return render(request, 'portfolio/research_detail.html', {
        'research': research,
        'student': student_profile,
        'is_owner': is_owner,
    })
    
def internship_detail(request, pk, matric_number):
    student_registry = get_object_or_404(StudentRegistry, matric_number=matric_number)
    student_profile = get_object_or_404(StudentProfile, registry=student_registry)
    internship = get_object_or_404(Internship, pk=pk, student=student_profile)

    is_owner = False
    if request.user.is_authenticated and hasattr(request.user, "studentprofile"):
        if request.user.studentprofile == student_profile:
            is_owner = True

    return render(request, 'portfolio/internship_detail.html', {
        'internship': internship,
        'student': student_profile,
        'is_owner': is_owner,
    })





def get_skills():
    return Skill.objects.all().order_by("name")

@login_required
def add_project(request):
    profile = StudentProfile.objects.get(user=request.user)
    skills = Skill.objects.all().order_by("name")
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = profile
            project.save()

            # Handle custom skills
            skill_ids = request.POST.getlist('skills')
            project.skills.set(skill_ids)

            messages.success(request, "Project added successfully.")
            return redirect('student_dashboard')
    else:
        form = ProjectForm()

    return render(request, 'portfolio/forms/project_form.html', {
        'form': form,
        'skills_json': skills_json,
    })


@login_required
def edit_project(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, pk=pk, student=profile)
    skills = get_skills()
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()

            # Handle custom skills
            skill_ids = request.POST.getlist('skills')
            project.skills.set(skill_ids)

            messages.success(request, "Project updated.")
            return redirect('student_dashboard')
    else:
        form = ProjectForm(instance=project)

    # Pass current project skill IDs as a comma-separated string for preloading (if needed in JS)
    selected_skill_ids = list(project.skills.values_list('id', flat=True))

    return render(request, 'portfolio/forms/project_form.html', {
        'form': form,
        'skills_json': skills_json,
        'selected_skill_ids': selected_skill_ids,
    })


@login_required
def add_research(request):
    profile = StudentProfile.objects.get(user=request.user)
    skills = get_skills()
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            research = form.save(commit=False)
            research.student = profile
            research.save()

            skill_ids = request.POST.getlist('skills')
            research.skills.set(skill_ids)

            messages.success(request, "Research added.")
            return redirect('student_dashboard')
    else:
        form = ResearchForm()

    return render(request, 'portfolio/forms/research_form.html', {
        'form': form,
        'skills_json': skills_json,
    })

@login_required
def edit_research(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    research = get_object_or_404(Research, pk=pk, student=profile)
    skills = get_skills()
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = ResearchForm(request.POST, request.FILES, instance=research)
        if form.is_valid():
            research = form.save()

            skill_ids = request.POST.getlist('skills')
            research.skills.set(skill_ids)

            messages.success(request, "Research updated.")
            return redirect('student_dashboard')
    else:
        form = ResearchForm(instance=research)

    selected_skill_ids = list(research.skills.values_list('id', flat=True))

    return render(request, 'portfolio/forms/research_form.html', {
        'form': form,
        'skills_json': skills_json,
        'selected_skill_ids': selected_skill_ids,
    })

@login_required
def add_internship(request):
    profile = StudentProfile.objects.get(user=request.user)
    skills = get_skills()
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.student = profile
            internship.save()

            skill_ids = request.POST.getlist('skills')
            internship.skills.set(skill_ids)

            messages.success(request, "Internship added.")
            return redirect('student_dashboard')
    else:
        form = InternshipForm()

    return render(request, 'portfolio/forms/internship_form.html', {
        'form': form,
        'skills_json': skills_json,
        'selected_skill_ids': []
    })

@login_required
def edit_internship(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    internship = get_object_or_404(Internship, pk=pk, student=profile)
    skills = get_skills()
    skills_json = serializers.serialize('json', skills, fields=('name',))

    if request.method == "POST":
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            internship = form.save()

            skill_ids = request.POST.getlist('skills')
            internship.skills.set(skill_ids)

            messages.success(request, "Internship updated.")
            return redirect('student_dashboard')
    else:
        form = InternshipForm(instance=internship)
        selected_skill_ids = list(internship.skills.values_list('id', flat=True))

    return render(request, 'portfolio/forms/internship_form.html', {
        'form': form,
        'skills_json': skills_json,
        'selected_skill_ids': selected_skill_ids
    })

@login_required
def delete_project(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, pk=pk, student=profile)
    project.delete()
    messages.success(request, "Project deleted.")
    return redirect('student_dashboard')


@login_required
def delete_research(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    research = get_object_or_404(Research, pk=pk, student=profile)
    research.delete()
    messages.success(request, "Research deleted.")
    return redirect('student_dashboard')


@login_required
def delete_internship(request, pk):
    profile = StudentProfile.objects.get(user=request.user)
    internship = get_object_or_404(Internship, pk=pk, student=profile)
    internship.delete()
    messages.success(request, "Internship deleted.")
    return redirect('student_dashboard')






