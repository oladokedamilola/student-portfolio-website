from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import *

# ===========================
# STUDENT REGISTRATION FLOW
# ===========================

def verify_matric(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT":
            return redirect('student_dashboard')
        elif request.user.role == "CLIENT":
            return redirect('client_dashboard')
        else:
            return redirect('home')

    """Step 1: Verify Matric Number"""
    if request.method == "POST":
        form = MatricVerificationForm(request.POST)
        if form.is_valid():
            matric = form.cleaned_data['matric_number']

            try:
                student_registry = StudentRegistry.objects.get(matric_number=matric)
            except StudentRegistry.DoesNotExist:
                messages.error(request, "❌ Matric number not found. Please double-check and try again.")
                return render(request, 'auth/verify_matric.html', {'form': form})

            if StudentProfile.objects.filter(registry=student_registry).exists():
                messages.error(request, "⚠️ This matric number has already been used to create an account. Please log in instead.")
                return redirect('login')

            # Success: Save verified matric to session
            request.session['verified_matric'] = matric
            messages.success(request, "✅ Matric number verified. Please proceed to create your account.")
            return redirect('student_register')
    else:
        form = MatricVerificationForm()

    return render(request, 'auth/verify_matric.html', {'form': form})


def student_register(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT":
            return redirect('student_dashboard')
        elif request.user.role == "CLIENT":
            return redirect('client_dashboard')
        else:
            return redirect('home')
    """Step 2: Register student account after matric verification"""
    matric = request.session.get('verified_matric')
    if not matric:
        messages.error(request, "No verified matric number found. Please verify your matric first.")
        return redirect('verify_matric')

    student_data = get_object_or_404(StudentRegistry, matric_number=matric)

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(email=email, password=password, role='STUDENT')
            StudentProfile.objects.create(user=user, registry=student_data)

            # Clear session to prevent reuse
            del request.session['verified_matric']

            messages.success(request, "🎉 Account created successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'auth/student_register.html', {
        'form': form,
        'student': student_data
    })

# ===========================
# CLIENT REGISTRATION FLOW
# ===========================

def client_register(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT":
            return redirect('student_dashboard')
        elif request.user.role == "CLIENT":
            return redirect('client_dashboard')
        else:
            return redirect('home')
        
    """Step 1: Client fills registration details"""
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            # Temporarily store in session
            request.session['client_registration_data'] = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'company_name': form.cleaned_data['company_name'],
                'industry': form.cleaned_data['industry'],
            }
            messages.info(request, "Almost done! Please verify your NIN to complete registration.")
            return redirect('verify_nin')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientRegistrationForm()
    return render(request, 'auth/client_register.html', {'form': form})


def verify_nin(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT":
            return redirect('student_dashboard')
        elif request.user.role == "CLIENT":
            return redirect('client_dashboard')
        return redirect('home')

    data = request.session.get('client_registration_data')
    if not data:
        messages.error(request, "⚠️ No registration data found. Please start again.")
        return redirect('client_register')

    if request.method == "POST":
        form = NINVerificationForm(request.POST)
        if form.is_valid():
            nin = form.cleaned_data['nin']

            try:
                nin_record = NINDatabase.objects.get(nin=nin)

                # Check if this NIN has already been used
                if ClientProfile.objects.filter(nin=nin_record).exists():
                    messages.error(request, "⚠️ This NIN has already been used to create an account.")
                    return redirect('client_register')

                # Match first and last names
                first_name_match = nin_record.first_name.strip().lower() == data['first_name'].strip().lower()
                last_name_match = nin_record.last_name.strip().lower() == data['last_name'].strip().lower()

                if not (first_name_match and last_name_match):
                    form.add_error(None, "❌ The names provided do not match our NIN records. Please check your details carefully.")
                else:
                    try:
                        user = User.objects.create_user(
                            email=data['email'],
                            password=data['password'],
                            role='CLIENT'
                        )

                        ClientProfile.objects.create(
                            user=user,
                            nin=nin_record,
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            company_name=data['company_name'],
                            industry=data['industry'],
                        )

                        login(request, user)
                        del request.session['client_registration_data']

                        messages.success(request, "✅ Your NIN has been verified and account created successfully! Welcome 🎉.")
                        return redirect('client_dashboard')

                    except Exception as e:
                        print("Error creating account:", e)
                        messages.error(request, "❌ Something went wrong while creating your account. Please try again.")
                        return redirect('client_register')

            except NINDatabase.DoesNotExist:
                form.add_error('nin', "❌ This NIN was not found. Please double-check your number.")
            except Exception as e:
                print("Unexpected verification error:", e)
                messages.error(request, "❌ An unexpected error occurred. Please try again later.")
                return redirect('client_register')

    else:
        form = NINVerificationForm()

    return render(request, 'auth/verify_nin.html', {'form': form})


# ===========================
# LOGIN
# ===========================

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT":
            return redirect('student_dashboard')
        elif request.user.role == "CLIENT":
            return redirect('client_dashboard')
        else:
            return redirect('home')
        
    """General login view for students and clients"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"👋 Welcome back, {user.email}!")
                if user.role == "STUDENT":
                    return redirect('student_dashboard')
                else:
                    return redirect('client_dashboard')
            else:
                messages.error(request, "❌ Invalid email or password. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

