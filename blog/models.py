from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок',
                             unique=True, db_index=True)
    content = models.TextField(verbose_name='Содержимое статьи',
                               blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='blog/images/', blank=True,
                              null=True)
    count_views = models.IntegerField(verbose_name='Количество просмотров',
                                      default=0)
    created_at = models.DateTimeField(verbose_name='Дата публикации',
                                      auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
