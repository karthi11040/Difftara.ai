from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.http import require_POST

def landing_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

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
        return redirect('dashboard')
    return render(request, 'accounts/signup.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')
import json
import re
from django.conf import settings
from django.http import JsonResponse

@require_POST
def firebase_login_view(request):
    try:
        token = json.loads(request.body).get('id_token', '')
        if not token or len(token) > 12000:
            return JsonResponse({'error': 'Invalid sign-in token.'}, status=400)
        import firebase_admin
        from firebase_admin import auth as firebase_auth
        from firebase_admin import credentials
        try:
            app = firebase_admin.get_app()
        except ValueError:
            cred_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT', '')
            credential = credentials.Certificate(cred_path) if cred_path else credentials.ApplicationDefault()
            app = firebase_admin.initialize_app(credential)
        claims = firebase_auth.verify_id_token(token, app=app, check_revoked=True)
        email = claims.get('email', '').strip().lower()
        if not email or not claims.get('email_verified'):
            return JsonResponse({'error': 'Use a verified email address to continue.'}, status=403)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(email__iexact=email).first()
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
        return JsonResponse({'error': 'Invalid sign-in request.'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Social sign-in is not configured on the server.'}, status=503)
