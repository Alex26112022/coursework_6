from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'content', 'preview', 'count_views',
                    'created_at']
    order_by = 'created_at'
    search_fields = ['title']
    list_display_links = ['pk', 'title', 'content']
    readonly_fields = ['preview']
    fields = ['title', 'content', 'image', 'preview']

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">')
