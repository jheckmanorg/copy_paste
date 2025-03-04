from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from .models import Paste
from .forms import SignUpForm, PasteForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('paste_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def paste_list(request):
    pastes = Paste.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    return render(request, 'pastes/list.html', {'pastes': pastes})

@login_required
def create_paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            paste = form.save(commit=False)
            paste.user = request.user
            paste.expires_at = timezone.now() + timedelta(minutes=30)
            paste.save()
            return redirect('paste_list')
    else:
        form = PasteForm()
    return render(request, 'pastes/create.html', {'form': form})

@login_required
@require_http_methods(['POST'])
def extend_paste(request, paste_id):
    paste = get_object_or_404(Paste, id=paste_id)
    
    if paste.user != request.user:
        raise PermissionDenied("You don't have permission to extend this paste.")
        
    current_time = timezone.now()
    
    if paste.expires_at <= current_time:
        messages.error(request, 'This paste has already expired.')
    elif paste.expires_at <= current_time + timedelta(hours=1):
        paste.expires_at += timedelta(minutes=30)
        paste.save()
        messages.success(request, 'Paste expiration extended by 30 minutes.')
    else:
        messages.warning(request, 'Paste cannot be extended. It still has more than an hour remaining.')
    
    return redirect('paste_list')
