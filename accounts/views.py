from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, login, logout
from django.contrib.auth.models import User


def verify_matric(request):
    if request.method == "POST":
        form = MatricVerificationForm(request.POST)
        if form.is_valid():
            matric = form.cleaned_data['matric_number']
            if StudentRegistry.objects.filter(matric_number=matric).exists():
                request.session['verified_matric'] = matric  # store temporarily
                return redirect('student_register')
            else:
                messages.error(request, "Matric number not found.")
    else:
        form = MatricVerificationForm()
    return render(request, 'auth/verify_matric.html', {'form': form})


def student_register(request):
    matric = request.session.get('verified_matric')
    if not matric:
        return redirect('verify_matric')

    student_data = StudentRegistry.objects.get(matric_number=matric)

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(email=email, password=password, role='STUDENT')
            StudentProfile.objects.create(
                user=user,
                registry=student_data  # Link to StudentRegistry directly
            )

            # Optional: clean up session
            del request.session['verified_matric']

            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'auth/student_register.html', {
        'form': form,
        'student': student_data
    })

def client_register(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            company_name = form.cleaned_data['company_name']
            industry = form.cleaned_data['industry']

            user = User.objects.create_user(email=email, password=password, role='CLIENT')
            ClientProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                industry=industry
            )
            messages.success(request, "Client account created. Please log in.")
            return redirect('login')
    else:
        form = ClientRegistrationForm()
    return render(request, 'auth/client_register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome, {user.email}")
                # Optional: redirect based on role
                if user.role == "STUDENT":
                    return redirect('student_dashboard')  # change to your URL
                else:
                    return redirect('client_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

