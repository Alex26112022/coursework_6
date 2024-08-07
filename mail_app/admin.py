from django.contrib import admin
from django.utils.safestring import mark_safe

from mail_app.models import Client, Newsletter, Message, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'slug', 'email', 'name', 'surname', 'father_name',
                    'status', 'created_at', 'owner']
    list_filter = ['status', 'owner']
    search_fields = ['name', 'surname', 'father_name', 'email', 'owner']
    list_display_links = ['pk', 'slug', 'email', 'name', 'surname',
                          'father_name', 'status', 'created_at', 'owner']
    fields = ['slug', 'photo', 'preview', 'email', 'name', 'surname',
              'father_name', 'comment', 'status']
    readonly_fields = ['preview']
    prepopulated_fields = {'slug': ('email',)}

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.photo.url}" style="max-height: 200px;">')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'slug', 'title', 'message', 'first_sent_at',
                    'last_sent_at', 'status', 'periodicity', 'count_sent',
                    'count_delivered', 'owner']
    list_filter = ['status', 'owner']
    search_fields = ['title', 'owner']
    list_display_links = ['pk', 'slug', 'title', 'message', 'first_sent_at',
                          'last_sent_at', 'status', 'periodicity',
                          'count_sent', 'count_delivered', 'owner']
    fields = ['slug', 'title', 'first_sent_at', 'last_sent_at', 'status',
              'periodicity', 'message', 'clients']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'theme', 'views_count', 'owner']
    list_display_links = ['pk', 'theme', 'views_count', 'owner']
    fields = ['theme', 'body', 'image', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'last_attempt_at', 'successfully', 'mail_response',
                    'newsletter']
    list_filter = ['successfully']
    list_display_links = ['pk', 'last_attempt_at', 'successfully',
                          'mail_response', 'newsletter']
