from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Blog, Category, Comment, Newsletter
from django.contrib import messages
from django.db.models import Count, Q

from django.core.paginator import Paginator


# Create your views here.

def home(request, category_slug=None):
    category = None

    posts = Blog.objects.filter(status='Published').order_by('-id')
    feature = Blog.objects.filter(exclusive='feature').order_by('-id')
    favourite = Blog.objects.filter(exclusive='favourite').order_by('-id')
    categories = Category.objects.all()
    categories = categories.annotate(total_post=Count('blog'))
    recent = posts.filter().order_by('-id')[0:2]
    
    
    

    
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        posts = posts.filter(category=category)

    if request.method == 'POST':
        email = request.POST.get('newsletter')
        newsletter = Newsletter.objects.create(email=email)
        messages.success(request, 'Welcome, You will be notified')
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        search_query = request.GET.get('Search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains = search_query)|
                Q(description__icontains = search_query)|
                #Q(user__icontains = search_query)|
                Q(category__name__icontains = search_query)
                )

    
        

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)


    context = {'posts': posts, 'feature': feature, 'favourite': favourite, 'categories': categories, 'recent': recent}

    return render(request, 'blog2.html', context)


def detail(request, detail_slug, category_slug=None):
    detail = Blog.objects.get(slug=detail_slug)
    category = None

    posts = Blog.objects.filter(status='Published').order_by('-id')
    feature = Blog.objects.filter(exclusive='feature').order_by('-id')
    favourite = Blog.objects.filter(exclusive='favourite').order_by('-id')
    categories = Category.objects.all()
    categories = categories.annotate(total_post=Count('blog'))
    recent = posts.filter().order_by('-id')[0:2]
    comments = Comment.objects.filter(post=detail).order_by('-id')
    total_comments = comments.count()

    if request.method == 'POST':
        body = request.POST.get('Message')
        comments = Comment.objects.create(post=detail, user=request.user, body=body)
        return redirect('blog:detail', detail.slug)
    
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        posts = posts.filter(category=category)


    
    if request.method == 'POST':
        email = request.POST.get('newsletter')
        newsletter = Newsletter.objects.create(email=email)
        messages.success(request, 'Welcome, You will be notified')
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        search_query = request.GET.get('Search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains = search_query)|
                Q(description__icontains = search_query)|
                #Q(user__icontains = search_query)|
                Q(category__name__icontains = search_query)
                )

    context = {'detail': detail, 'posts': posts, 'feature': feature, 'favourite': favourite, 'categories': categories, 'recent': recent, 'comments': comments, 'total_comments': total_comments}

    return render(request, 'single.html', context)