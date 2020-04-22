from datetime import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from mdeditor.fields import MDTextField


User = get_user_model()

class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='标签名称', max_length=30)
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='分类名称', max_length=30)
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)

    class Meta:
        db_table = 'tb_category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章
    """
    ARTICLE_STYLE = (
        [0, '仅摘要'],
        [1, '图片置顶'],
        [2, '图片居中'],
        [3, '仅正文'],
    )

    IS_SHOW = (
        [0, '否'],
        [1, '是'],
    )

    IS_SEARCH = (
        [0, '否'],
        [1, '是'],
    )

    title = models.CharField(verbose_name='标题', max_length=150, validators=[MinLengthValidator(1), ])
    digest = models.TextField(verbose_name='摘要', null=True, blank=True)
    content = MDTextField(verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.SET_NULL, default=1, null=True, blank=True)
    image = models.ImageField(verbose_name='封面图片', upload_to='media/image/', null=True, blank=True)
    style = models.SmallIntegerField(verbose_name='首页展示风格', choices=ARTICLE_STYLE, default=0, null=True, blank=True)
    sidebar = models.SmallIntegerField(verbose_name='启用内页导航', choices=IS_SHOW, default=0, null=True, blank=True)
    search = models.SmallIntegerField(verbose_name='是否创建搜索此文章', choices=IS_SEARCH, default=0, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')
    clicks = models.IntegerField(verbose_name='点击量', default=0, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)

    def increase_views(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    class Meta:
        ordering = ['-id']
        db_table = 'tb_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comments(models.Model):
    """
    评论
    """
    READ_CHOICES = [
        [0, '否'],
        [1, '是']
    ]

    MAIL_CHOICES = [
        [0, '否'],
        [1, '是']
    ]

    article = models.ForeignKey(Article, verbose_name='文章评论', on_delete=models.CASCADE, related_name='comment')
    content = models.TextField(verbose_name='评论内容')
    author = models.CharField(verbose_name='评论作者', max_length=12)
    parent = models.ForeignKey('self', verbose_name='父级评论', on_delete=models.CASCADE, related_name='child', null=True, blank=True)
    mail = models.EmailField(verbose_name='邮箱')
    url = models.CharField(verbose_name='站点地址', max_length=64, null=True, blank=True)
    re_mail = models.SmallIntegerField(verbose_name='邮件通知', choices=MAIL_CHOICES, default=1, null=True, blank=True)
    is_read = models.SmallIntegerField(verbose_name='是否已读', choices=READ_CHOICES, default=0, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)

    class Meta:
        ordering = ['-id']
        db_table = 'tb_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author

    def child_list(self):
        child_list = []
        for comment in self.child.all():
            if comment.child.all():
                child_list.extend(comment.child_list())
                child_list.append(comment)
            else:
                child_list.append(comment)
        return child_list


class CommentsVote(models.Model):
    """
    评论点赞
    """
    comment = models.OneToOneField(Comments, on_delete=models.CASCADE, related_name='vote')
    up = models.IntegerField(null=True, blank=True, default=0)
    down = models.IntegerField(null=True, blank=True, default=0)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'tb_comments_vote'
        verbose_name = '评论点赞'
        verbose_name_plural = verbose_name


class ArticleVote(models.Model):
    """
    文章点赞
    """
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='vote')
    up = models.IntegerField(verbose_name='点赞数', null=True, blank=True, default=0)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'tb_article_vote'
        verbose_name = '文章点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.up)


