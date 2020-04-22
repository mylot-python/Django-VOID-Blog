from django.contrib import admin
from django.utils.html import format_html

from . import models

class BangumiAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'num', 'status', 'count', 'edit_button']
    ordering = ('id',)
    list_per_page = 20
    list_display_links = None
    fieldsets = (
        (None, {'fields': ('name', 'num', 'status', 'count')}),
    )

    def edit_button(self, obj):
        link = '/admin/bangumi/bangumimodel/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    class Media:
        css = ({'all': ['css/button.css']})

    edit_button.short_description = '操作'

admin.site.register(models.BangumiModel, BangumiAdmin)