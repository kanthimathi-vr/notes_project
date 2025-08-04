from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .models import Note
from .forms import RegisterForm, NoteForm

class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('note_list')
    return render(request, 'myapp/register.html', {'form': form,'title':'Register'})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'myapp/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False); note.user = request.user; note.save()
        return redirect('note_list')
    return render(request,'myapp/note_form.html',{'form':form,'title':'New Note'})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save(); return redirect('note_list')
    return render(request,'myapp/note_form.html',{'form':form,'title':'Edit Note'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete(); return redirect('note_list')
    return render(request,'myapp/note_confirm_delete.html',{'note': note})
