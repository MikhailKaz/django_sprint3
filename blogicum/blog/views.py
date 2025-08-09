from datetime import datetime, timezone
from django.shortcuts import get_object_or_404, render
from .models import Category, Post


def get_posts():
    """Вспомогательная функция для получения постов."""
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now(timezone.utc),
    ).select_related('author', 'category', 'location')


def index(request):
    context = {
        'post_list': get_posts()[:5],
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    context = {
        'post': get_object_or_404(get_posts(), pk=id),
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {
        'category': category,
        'post_list': get_posts().filter(category__pk=category.pk),
    }
    return render(request, 'blog/category.html', context)
