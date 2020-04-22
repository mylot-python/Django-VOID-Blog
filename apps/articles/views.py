import json, logging, mistune, os, time

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, render_to_response
from django.views import View
from django.http import HttpResponse, JsonResponse

from .forms import CommentsForm
from . import models

logger = logging.getLogger('django')

def page_not_found(request):
    context = {
        'cls': models.Category.objects.all(),
    }
    return render_to_response('404.html', context=context)

def page_paginator(request, obj):
    # 分页操作
    try:
        page = int(request.GET.get('page', 1))  # 默认显示第一页
    except Exception as e:
        logger.error("当前页数错误：\n{}".format(e))
        # 如果参数有误, 默认显示第一页
        page = 1
    # 使用django自带的分页模块
    paginator = Paginator(obj, 10)

    try:
        obj_query = paginator.page(page)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，触发EmptyPage空页错误, 则返回最后一页数据
        logging.info("用户访问的页数大于总页数。")
        # num_pages表示最后一页, 说明如果前端发送的请求超过最大页数, 则返回最后一页
        obj_query = paginator.page(paginator.num_pages)
    return obj_query


class IndexView(View):
    """
    首页
    """

    def get(self, request):
        # 获取文章
        article = models.Article.objects.select_related('author').only(
            'id', 'title', 'digest', 'image', 'update_time', 'style',
            'content', 'author__username',
        ).filter(is_delete=False)
        article_query = page_paginator(request, article)
        context = {
            'article': article_query,
            'cls': models.Category.objects.all(),
        }
        return render(request, 'articles/index.html', context=context)


class ArticleDetail(View):
    """
    文章详情
    route: /article/<int:article_id>/
    """
    def get(self, request, article_id):
        # 获取对应文章
        article = models.Article.objects.select_related('author', 'vote').defer(
            'create_time', 'is_delete', 'search', 'category'
        ).filter(id=article_id, is_delete=False).first()

        if article:
            # 使用大于等于过滤出上一篇和下一篇
            next = models.Article.objects.only('id', 'title', 'digest').filter(
                id__gt=article_id, is_delete=False
            ).first()
            prev = models.Article.objects.only('id', 'title', 'digest').filter(
                id__lt=article_id,is_delete=False
            ).first()
            # 渲染文章为markdown格式
            article.content = mistune.markdown(article.content)
            # 触发文章阅读+1
            models.Article.increase_views(article)
            # 获取当前文章的所有评论
            all_comments = models.Comments.objects.select_related('vote').only(
                'id', 'content', 'author', 'update_time', 'parent', 'url', 'mail', 'parent',
                'vote__up', 'vote__down'
            ).filter(article_id=article_id,is_delete=False).order_by('-update_time')
            # 获取parent=None的一级评论
            comments = all_comments.filter(parent=None)
            # 对评论分页
            comments_query = page_paginator(request, comments)
            context = {
                'comments_query': comments_query,
                'comments_count': len(all_comments),
                'article': article,
                'next': next,
                'prev': prev,
                'cls': models.Category.objects.all(),
            }
            return render(request, 'articles/article.html', context=context)
        else:
            return HttpResponse('err')


class ArticleComments(View):
    """
    评论
    route: /comments/<int:article_id>
    """

    def post(self, request, id):

        if not models.Article.objects.only('id').filter(id=id).exists():
            return JsonResponse({"code": 404, "errmsg": "新闻不存在!"})

        author = request.POST.get('author')
        mail = request.POST.get('mail')
        parent = request.POST.get('parent')
        content = request.POST.get('text')
        url = request.POST.get('url')
        re_Mail = True if request.POST.get('receiveMail') == 'yes' else False

        if request.user.is_staff == False:
            # 判断非登录状态下不允许使用的邮箱和用户名
            if mail == '4520392@qq.com' or author == '无风清响':
                return JsonResponse({"code": 404, "errmsg": "你的用户名或者邮箱与作者相同, 请勿重复!"})

        try:
            data = {
                'article': id,
                'content': content,
                'author': author,
                'parent': parent,
                'mail': mail,
                'url': url,
                're_mail': re_Mail,
                'is_read': True if request.user.is_staff else False
            }
            form = CommentsForm(data=data)

            if form.is_valid():
                comment = form.save()
                vote = models.CommentsVote()
                vote.comment = comment
                vote.save()
                if request.user.is_staff and comment.parent:
                    parent = comment.parent
                    parent.is_read = True
                    parent.save(update_fields=['is_read'])
                data = {
                    're_author': author,
                    're_mail': mail,
                    're_url': url
                }
                return JsonResponse({'code': 200, 'data': data})
            else:
                # 定义一个错误信息列表
                err_msg_list = []
                for item in form.errors.get_json_data().values():
                    err_msg_list.append(item[0].get('message'))
                # 拼接错误信息为一个字符串
                err_msg_str = '/'.join(err_msg_list)
                return JsonResponse({"code": 404, "errmsg": err_msg_str})
        except Exception as e:
            logging.info('保存评论错误: {}'.format(e))
            return JsonResponse({"code": 404, "errmsg": "传来的数据有误!"})


class ArticleVote(View):
    """
    点赞
    route: /vote/
    """

    def post(self, request):
        try:
            json_data = request.body
            if not json_data:
                return JsonResponse({"code": 404})
            dict_data = json.loads(json_data.decode('utf8'))
            id = int(dict_data.get('id'))
            type = dict_data.get('type')
            choose = dict_data.get('choose')
        except Exception as e:
            logging.info('错误信息: {}'.format(e))
            return JsonResponse({"code": 404})
        obj_dict = {
            'comment': models.Comments.objects,
            'content': models.Article.objects
        }
        obj = obj_dict.get(choose).only('id').filter(id=id).first()

        if not obj:
            return JsonResponse({"code": 404})

        try:
            if choose == 'comment':
                vote = models.CommentsVote.objects.get_or_create(comment=obj)[0]
            elif choose == 'content':
                vote = models.ArticleVote.objects.get_or_create(article=obj)[0]
            else:
                return JsonResponse({"code": 404})
            if type == 'up':
                vote.up += 1
                vote.save(update_fields=['up'])
            # 文章没有down
            elif type == 'down' and choose == 'comment':
                vote.down += 1
                vote.save(update_fields=['down'])
            else:
                return JsonResponse({"code": 404})
            return JsonResponse({"code": 200})
        except Exception as e:
            logging.info('错误信息: {}'.format(e))
            return JsonResponse({"code": 404})


class ArticleForTag(View):
    """
    包含标签的文章
    route: /tag/<str:tag_name>/
    """

    def get(self, request, tag_name):
        article = models.Article.objects.select_related('author').only(
            'id', 'title', 'digest', 'image', 'create_time', 'update_time',
            'style', 'content', 'author__username'
        ).filter(is_delete=False, tag__name=tag_name)
        article_query = page_paginator(request, article)
        context = {
            'article': article_query,
            'tag_name': tag_name,
            'cls': models.Category.objects.all(),
        }
        return render(request, 'articles/index.html', context=context)


class ArticleForCategory(View):
    """
    包含分类的文章
    route: /category/<str:cls_name>/
    """

    def get(self, request, cls_name):
        article = models.Article.objects.select_related('author').only(
            'id', 'title', 'digest', 'image', 'create_time', 'update_time',
            'style', 'content', 'author__username'
        ).filter(is_delete=False, category__name=cls_name)
        article_query = page_paginator(request, article)
        context = {
            'article': article_query,
            'cls_name': cls_name,
            'cls': models.Category.objects.all(),
        }
        return render(request, 'articles/category.html', context=context)


class ArticleArchives(View):
    """
    create archives view
    route: /archives/
    """

    def get(self, request):
        # 获取今年
        this_year = int(time.strftime("%Y", time.localtime()))
        # 获取文章
        article_query = models.Article.objects.only(
            'id', 'title', 'content', 'create_time'
        ).filter(is_delete=False).order_by('create_time')

        if article_query:
            # 统计文章数
            article_count = article_query.count()
            # 统计分类数
            cls_count = models.Category.objects.only('id').count()
            # 年列表
            year_list = []
            last_yaer = int(article_query.last().create_time.strftime("%Y"))
            first_year = int(article_query.first().create_time.strftime("%Y"))
            gap = last_yaer - first_year
            if gap != 0:
                for i in range(gap+1):
                    year_list.append(first_year)
                    first_year = first_year + 1
            else:
                year_list.append(last_yaer)
            article_set = {}
            for i in year_list:
                article_set.setdefault(i, article_query.filter(create_time__year=i))
            tags = models.Tag.objects.only('name').all()
            context = {
                'this_year': this_year,
                'article_set': article_set,
                'year_list': year_list,
                'tags': tags,
                'article_count': article_count,
                'cls_count': cls_count,
                'cls': models.Category.objects.all(),
            }
        else:
            context = {}
        return render(request, 'articles/archives.html', context=context)


class SearchJson(View):

    def get(self, request):
        try:
            with open(os.getcwd() + '/static/json/ExSearch.json', 'r') as file:
                json_data = json.load(file)
                # 解决跨域问题
                # res = HttpResponse(json.dumps(json_data))
                # # obj['Access-Control-Allow-Origin']='*'
                # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
                # return res
                return JsonResponse(json_data, safe=False)
        except Exception as e:
            logger.info('获取search.json失败: {}'.format(e))
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
            # return res
            return JsonResponse({}, safe=False)