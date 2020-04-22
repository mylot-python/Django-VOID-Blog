from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from . import models


class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'list_num', 'server', 'edit_button']
    list_per_page = 20
    list_display_links = None
    fieldsets = (
        (None, {'fields': ('list_num', 'server')}),
    )

    def edit_button(self, obj):
        link = '/admin/music/musicmodel/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    class Media:
        css = ({'all': ['css/button.css']})

admin.site.register(models.MusicModel, MusicAdmin)