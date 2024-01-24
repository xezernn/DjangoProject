from django.shortcuts import render, get_object_or_404
from django.db.models import Q 
from .models import Category, Post, Author
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        comment_form = CommentForm()
    context = {
        'post': post,
        'latest': latest,
        'form': comment_form,
    }


    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

# def search(request):
#     queryset = Post.objects.all()
#     query = request.GET.get('q')
#     # print(queryset)
#     if query:
#         print(queryset.query)
#         queryset = queryset.filter(
#             Q(title=query) 
#             # |
#             # Q(overview__icontains=query)
#         ).distinct()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, 'search_bar.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
    # Örnek olarak başlıkta olabilecek boşlukları temizleyebilirsiniz
        cleaned_query = query.strip()
        queryset = queryset.filter(
            Q(title__icontains=cleaned_query)
    ).distinct()

    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)

def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)


def LikeView (request,slug):
    post = get_object_or_404(Post, id = request.POST.get("post_id"))
    post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post', args = [str(slug)]))