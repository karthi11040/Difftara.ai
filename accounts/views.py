from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.http import require_POST

def landing_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')
        password_input = request.POST.get('password')
        user = authenticate(request, username=user_input, password=password_input)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/signup.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')
import json
import re
from django.http import JsonResponse

@require_POST
def firebase_login_view(request):
    try:
        payload = json.loads(request.body)
        if not isinstance(payload, dict):
            return JsonResponse({'error': 'Invalid sign-in request.'}, status=400)
        token = payload.get('id_token', '')
        if not token or len(token) > 12000:
            return JsonResponse({'error': 'Invalid sign-in token.'}, status=400)
        from google.auth.transport.requests import Request as GoogleAuthRequest
        from google.oauth2 import id_token
        claims = id_token.verify_firebase_token(token, GoogleAuthRequest(), audience='difftara-ai-139ec')
        email = claims.get('email', '').strip().lower()
        if not email or not claims.get('email_verified'):
            return JsonResponse({'error': 'Use a verified email address to continue.'}, status=403)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(email__iexact=email).first()
        if user and not user.is_active:
            return JsonResponse({'error': 'This account is disabled. Contact your administrator.'}, status=403)
        if user is None:
            base = re.sub(r'[^a-zA-Z0-9_.-]', '', email.split('@')[0])[:120] or 'user'
            username, suffix = base, 1
            while User.objects.filter(username=username).exists():
                suffix += 1
                username = f'{base[:120-len(str(suffix))]}{suffix}'
            user = User.objects.create_user(username=username, email=email)
        login(request, user)
        return JsonResponse({'ok': True})
    except (ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'This sign-in token is invalid or expired. Please sign in again.'}, status=401)
    except Exception as exc:
        from google.auth.exceptions import GoogleAuthError
        if isinstance(exc, GoogleAuthError):
            return JsonResponse({'error': 'Identity verification is temporarily unavailable. Please try again.'}, status=503)
        return JsonResponse({'error': 'Sign-in could not be completed. Please try again.'}, status=503)
