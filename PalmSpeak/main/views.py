from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import uuid
import os
import subprocess
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import re
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm


logger = logging.getLogger(__name__)

def home_page(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('/home/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified. Check your mail.')
            return redirect('/home/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong password.')
            return redirect('/home/login')

        login(request, user)
        return redirect('/home/service')

    return render(request, 'login.html')

import re

def is_password_complex(password):
    # Define your password complexity criteria
    # For example, at least 8 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*()-_+=]", password):
        return False
    return True

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        
        # Check password complexity
        if not is_password_complex(password):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
            return redirect('/home/register')

    try:
        if User.objects.filter(username=username).first():
            messages.success(request, 'Username is already taken.')
            return redirect('/home/register')

        if User.objects.filter(email=email).first():
            messages.success(request, 'Email is already taken.')
            return redirect('/home/register')
        
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()
        send_mail_after_registration(email, auth_token, 'registration')
        return redirect('token_send/')

    except Exception as e:
        print(e)
    return render(request,'registeration.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            # Generate reset token
            profile_obj = Profile.objects.get(user=user)
            auth_token = str(uuid.uuid4())
            profile_obj.auth_token = auth_token
            profile_obj.save()
            
            # Send email with reset link
            send_mail_after_registration(email, auth_token, 'reset')
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('token_send/')  # Redirect to login page
        else:
            messages.error(request, 'No user with this email exists.')
    return render(request, 'forgetPass.html')

@login_required
def success_page(request):
    return render(request, 'success.html')

def token_send_page(request):
    return render(request, 'token_send.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/home/login/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/home/login/')
        else:
            return redirect('/home/error/')
    except Exception as e:
        print(e)
        return redirect('/')

def verify_reset_token(request, auth_token):
    print(f"Received auth_token: {auth_token}")  # Debug print statement
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if request.method == 'POST':
            password = request.POST.get('newPass')
            confirm_password = request.POST.get('confirmpass')
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/home/verify_reset/{auth_token}')
            
            user = profile_obj.user
            # Update user's password
            user.set_password(password)
            user.save()
            profile_obj.auth_token = ''
            profile_obj.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('/home/login/')  # Redirect to login page
        else:
            return render(request, 'resetPassword.html', {'auth_token': auth_token})
    else:
        messages.error(request, 'Invalid token.')
        return redirect('/home/error/')

def error(request):
    return render(request, 'error.html')

def about_us(request):
    return render(request, 'indAboutUs.html')

def contact_us(request):
    return render(request, 'indContactUs.html')

def send_mail_after_registration(email, token, mail_type):
  try:
    if mail_type == 'registration':
        subject = 'Your account needs to be verified'
        message = f'Hi, paste the link to verify your account: http://127.0.0.1:8000/home/verify/{token}'
        print('Email sent successfully')
    elif mail_type == 'reset':
        subject = 'Password Reset Request'
        message = f'Hi, click the link to reset your password: http://127.0.0.1:8000/home/verify_reset/{token}'
    print(f'Sending email to {email} with reset link: {message}')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    print('Email sent successfully')

  except Exception as e:
        print(f'Failed to send email: {e}')

def send_reset_password_email(email, token):
    subject = 'Reset Your Password'
    message = f'Hi, click the link to reset your password: http://127.0.0.1:8000/home/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

@login_required
def service(request):
    if not request.user.is_authenticated:
        print("User is not authenticated, redirecting to login")
        return redirect('home/login/')  # Redirect to the login page if not authenticate

    if request.method == 'POST':
        logger.info("execute_code function called")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Notebooks', 'Name.py'))
        logger.info("Script path: %s", script_path)

        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            logger.error("Error executing script: %s", error.decode('utf-8'))
            print("Error executing script:", error.decode('utf-8'))
        else:
            logger.info("Script executed successfully")
            print("Script executed successfully")

    return render(request, 'service.html')

