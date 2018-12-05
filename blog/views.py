"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from blog.models import Post


def blog_list(request):
    """
    Purpose: Retrieve published blog post(s)
    :param request: incoming request
    :return: rendered HTML template with published post(s)
    """
    posts_obj = Post.objects.filter(published=True)
    paginator = Paginator(object_list=posts_obj, per_page=5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(number=page)
    except PageNotAnInteger:
        posts = paginator.page(number=1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request=request, template_name='blog/list.html', context={
        'posts': posts
    })


def blog_detail(request, slug):
    """
    Purpose: Retrieve detailed blog post, must be published
    :param request: incoming request
    :param slug: beautiful slug URL (post title)
    :return: rendered HTML template with detailed post
    """
    post = get_object_or_404(klass=Post, slug=slug, published=True)
    return render(request=request, template_name='blog/detail.html', context={
        'post': post
    })
