from django.contrib import admin
from django.utils.safestring import mark_safe

from mail_app.models import Client, Newsletter, Message, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'name', 'surname', 'father_name',
                    'status', 'created_at', 'newsletter']
    list_filter = ['status']
    search_fields = ['name', 'surname', 'father_name', 'email']
    list_display_links = ['pk', 'email', 'name', 'surname', 'father_name',
                          'status', 'created_at', 'newsletter']
    fields = ['photo', 'preview', 'email', 'name', 'surname', 'father_name',
              'comment', 'status', 'newsletter']
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.photo.url}" style="max-height: 200px;">')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'message', 'first_sent_at', 'status',
                    'periodicity', 'count_sent', 'count_delivered',
                    'count_transition']
    list_filter = ['status']
    search_fields = ['title']
    list_display_links = ['pk', 'title', 'first_sent_at', 'status',
                          'periodicity',
                          'count_sent', 'count_delivered', 'count_transition',
                          'message']
    fields = ['title', 'status', 'periodicity', 'message']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'theme']
    list_display_links = ['pk', 'theme']
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
