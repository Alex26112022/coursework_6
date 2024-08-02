import random

from django.shortcuts import render
from django.views.generic import DetailView

from blog.models import Blog
from mail_app.models import Newsletter, Client


def index(request):
    """ Главная страница сайта. """
    newsletters = Newsletter.objects.all()
    newsletters_active = Newsletter.objects.filter(status='Запущена')
    clients = Client.objects.all()
    blogs = Blog.objects.all()
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
        obj = super().get_object(queryset)
        obj.count_views += 1
        obj.save()
        return obj
