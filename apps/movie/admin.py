from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from movie import models


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'num', 'status', 'edit_button']
    list_per_page = 20
    list_display_links = None
    fieldsets = (
        (None, {'fields': ('name', 'num', 'status')}),
    )

    def edit_button(self, obj):
        link = '/admin/movie/moviemodel/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    class Media:
        css = ({'all': ['css/button.css']})

admin.site.register(models.MovieModel, MovieAdmin)