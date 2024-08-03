import random

from django.shortcuts import render
from django.views.generic import DetailView

from blog.models import Blog
from blog.services import get_from_cache


def index(request):
    """ Главная страница сайта. """
    content_cache = get_from_cache()
    newsletters = content_cache[0]
    newsletters_active = content_cache[1]
    clients = content_cache[2]
    blogs = content_cache[3]
    if blogs:
        blog_list = []
        while True:
            random_blog = random.choice(blogs)
            if random_blog not in blog_list:
                blog_list.append(random_blog)
                if len(blog_list) == 3:
                    break
        blogs = blog_list
    count_newsletters = len(newsletters)
    count_newsletters_active = len(newsletters_active)
    count_clients = len(clients)

    context = {'count_newsletters': count_newsletters,
               'count_newsletters_active': count_newsletters_active,
               'count_clients': count_clients,
               'blogs': blogs}
    return render(request, 'blog/index.html', context)


class BlogDetailView(DetailView):
    """ Выводит подробную информацию о блоге. """
    model = Blog

    def get_object(self, queryset=None):
        """ Добавляет информацию о просмотрах блога. """
        obj = super().get_object(queryset)
        obj.count_views += 1
        obj.save()
        return obj
