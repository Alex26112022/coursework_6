from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED
from mail_app.models import Newsletter, Client


def get_from_cache():
    """ Получает список данные из кэша или из БД. """
    if not CACHE_ENABLED:
        return Newsletter.objects.all(), Newsletter.objects.filter(
            status='Запущена'), Client.objects.all(), Blog.objects.all()

    key1 = 'newsletter_list'
    key2 = 'newsletter_active_list'
    key3 = 'client_list'
    key4 = 'blog_list'

    newsletters = cache.get(key1)
    newsletters_active = cache.get(key2)
    clients = cache.get(key3)
    blog = cache.get(key4)

    if newsletters is not None and newsletters_active is not None and clients is not None and blog is not None:
        return newsletters, newsletters_active, clients, blog

    newsletters = Newsletter.objects.all()
    newsletters_active = Newsletter.objects.filter(
        status='Запущена')
    clients = Client.objects.all()
    blog = Blog.objects.all()

    cache.set(key1, newsletters)
    cache.set(key2, newsletters_active)
    cache.set(key3, clients)
    cache.set(key4, blog)
    return newsletters, newsletters_active, clients, blog
