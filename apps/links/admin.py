from django.contrib import admin
from django.utils.html import format_html

from . import models

class LinksAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'site_name', 'status', 'link_img', 'edit_button']
    ordering = ('id',)
    fieldsets = (
                    (('详情'), {'fields': ('name', 'site_name', 'status', 'text')}),
                    (('链接'), {'fields': ('site_url', 'image_url')}),
                 )

    class Media:
        css = ({'all': ['css/button.css']})

    def link_img(self, obj):
        img = '<img src="{}" height="50" width="50">'.format(obj.image_url)
        return format_html(img)

    def edit_button(self, obj):
        link = '/admin/links/linksmodel/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)


    link_img.short_description = '头像'
    edit_button.short_description = '操作'


admin.site.register(models.LinksModel, LinksAdmin)