from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import login as auth_login

# Create your views here.
def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(req, 'includes/signup.html', {'form':form})