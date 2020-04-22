import json, os, logging, re

logger = logging.getLogger('django')

article_url = 'https://www.breezed.cn/article/'
tags_url = 'https://www.breezed.cn/tag/'
category_url = 'https://www.breezed.cn/category/'

tree = {
    "posts": [
    ],
    "pages": [
        {
            "title": "观影",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/movie/",
            "text": ""
        },
        {
            "title": "追番",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/bangumi/",
            "text": ""
        },
        {
            "title": "阅读",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/book/",
            "text": ""
        },
        {
            "title": "音乐",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/music/",
            "text": ""
        },
        {
            "title": "友链",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/links/",
            "text": ""
        },
        {
            "title": "归档",
            "date": "2019-10-10T10:10:00+10:00",
            "path": "https://www.breezed.cn/archives/",
            "text": ""
        }
    ]
}


def WriteSearchV2(value):
    article = value
    try:
        # 如果json文件不存在, 会报错, 故此使用try
        with open(os.getcwd() + '/static/json/ExSearch.json', 'r') as json_file:
            open_file = json.load(json_file)
    except Exception as e:
        logger.error("打开文件失败: {}".format(e))
        open_file = tree

    posts = open_file['posts']
    for post in posts:
        if article.title in post['title']:
            index = posts.index(post)
            del posts[index]
            try:
                open_file['posts'] = posts
                with open(os.getcwd() + '/static/json/ExSearch.json', 'w') as json_file:
                    json.dump(open_file, json_file)
            except Exception as e:
                logger.info('{}文章修改失败: {}'.format(article.title, e))
            break

    if article.search == 0:
        return
    ex_title = article.title
    ex_date = article.update_time.strftime("%Y-%m-%d %H:%M:%S")
    ex_path = article_url + '{}/'.format(article.id)
    filtrate = re.compile(u'#+|`+|"{3}|-+|\s+')
    ex_text = filtrate.sub(r'', article.content[:200])
    ex_tags = [
        {
            'name': i.name,
            'slug': i.name,
            'permalink': tags_url + '{}/'.format(i)
        } for i in article.tag.all()
    ]
    ex_category = [
        {
             'name': article.category.name,
             'slug': article.category.name,
             'permalink': category_url + '{}/'.format(article.category)
         }
    ]
    ex_dict = {
        "title": ex_title,
        "date": ex_date,
        "path": ex_path,
        "text": ex_text,
        "tags": ex_tags,
        "categories": ex_category
    }
    try:
        open_file['posts'].append(ex_dict)
        with open(os.getcwd() + '/static/json/ExSearch.json', 'w') as json_file:
            json.dump(open_file, json_file)
    except Exception as e:
        logger.info('{}文章ex写入失败: {}'.format(ex_title, e))
    return



