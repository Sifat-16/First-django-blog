from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm
from blog.models import Blog, Category, Comment, Newsletter
from django.db.models import Q


# Create your views here.

def loginpage(request):
    recent = Blog.objects.filter(status='Published').order_by('-id')[0:2]
    posts = Blog.objects.filter(status='Published').order_by('-id')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Incorrect username or password')

    

    if request.method == 'POST':
        email = request.POST.get('newsletter')
        newsletter = Newsletter.objects.create(email=email)
        messages.success(request, 'Welcome, You will be notified')
        return redirect('accounts:signup')

    search_query = request.GET.get('Search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains = search_query)|
            Q(description__icontains = search_query)|
            #Q(user__icontains = search_query)|
            Q(category__name__icontains = search_query)
            )

    context = {'recent': recent}

    return render(request, 'registration/login.html', context)


def signuppage(request):
    recent = Blog.objects.filter(status='Published').order_by('-id')[0:2]
    posts = Blog.objects.filter(status='Published').order_by('-id')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignUpForm()

    if request.method == 'POST':
        email = request.POST.get('newsletter')
        newsletter = Newsletter.objects.create(email=email)
        messages.success(request, 'Welcome, You will be notified')
        return redirect('accounts:login')

    search_query = request.GET.get('Search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains = search_query)|
            Q(description__icontains = search_query)|
            #Q(user__icontains = search_query)|
            Q(category__name__icontains = search_query)
            )

    
    context = {'form': form, 'recent': recent}
    return render(request, 'registration/register.html', context)


def logout_request(request):
    logout(request)
    return redirect('blog:home')