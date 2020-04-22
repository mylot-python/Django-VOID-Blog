from django.contrib import admin

from django.utils.html import format_html

from articles import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'clicks', 'vote', 'update_time', 'category', 'my_tag', 'my_comment', 'edit_button']
    list_display_links = None
    ordering = ('-id', )
    list_per_page = 20
    fieldsets = (
                    (('标题'), {'fields': ('title', 'digest',)}),
                    (('功能选择'), {'fields': ('tag', 'category', 'style', 'sidebar', 'search')}),
                    (('内容详情'), {'fields': ('image', 'content', )}),
                    (('删除控制'), {'fields': ('is_delete', )}),
                 )

    filter_horizontal = ('tag',)
    # inlines = [CommentsStackedInline]
    list_filter = ('title', 'tag', 'category', 'is_delete', 'create_time')

    def my_tag(self, obj):
        return '/'.join([t.name for t in obj.tag.all()])

    def my_comment(self, obj):
        return len(obj.comment.all())

    def edit_button(self, obj):
        link = '/admin/articles/article/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    class Media:
        css = ({'all': ['css/button.css']})

    my_tag.short_description = '标签'
    my_comment.short_description = '评论数'
    edit_button.short_description = '操作'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'edit_button']
    list_display_links = None
    ordering = ('id',)
    fieldsets = ((None, {'fields': ('name', 'is_delete',)}),)

    def edit_button(self, obj):
        link = '/admin/articles/category/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    class Media:
        css = ({'all': ['css/button.css']})

    edit_button.short_description = '操作'


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'edit_button']
    ordering = ('id',)
    fieldsets = ((None, {'fields': ('name', 'is_delete',)}),)

    class Media:
        css = ({'all': ['css/button.css']})

    def edit_button(self, obj):
        link = '/admin/articles/tag/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    edit_button.short_description = '操作'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'author', 'parent', 're_mail', 'is_read', 'edit_button']
    ordering = ('-id',)
    list_per_page = 20
    list_display_links = None
    fieldsets = (
        ('详情', {'fields': ('article', 'content')}),
        ('评论者', {'fields': ('author', 'parent')}),
        ('关联', {'fields': ('mail', 'url')}),
        ('状态', {'fields': ('re_mail', 'is_read', 'is_delete')}),
    )

    list_filter = ('article', 'create_time', 'is_delete')

    class Media:
        css = ({'all': ['css/button.css']})

    def edit_button(self, obj):
        link = '/admin/articles/comments/{}/change/'.format(obj.id)
        btn_str = '<a type="button" href="{}">' \
                  '<button type="button" class="button" title="编辑" name="index">编辑</button>' \
                  '</a>'
        return format_html(btn_str, link)

    edit_button.short_description = '操作'


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comments, CommentAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Category, CategoryAdmin)