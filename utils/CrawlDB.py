import json, logging, requests, urllib3, os

from lxml import etree

logger = logging.getLogger('django')
header = {
    'Referer': 'https://www.baidu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def CrawlDBMovie(value, sta):
    num = value
    status = sta
    if status not in ['wish', 'watched']:
        return {"code": 404, "errmsg": "影片分类不正确"}
    url = 'https://movie.douban.com/subject/{}/'.format(num)
    urllib3.disable_warnings()

    try:
        # 构造爬虫, 爬取番剧数据
        print('------------爬虫开始-------------')
        res = requests.get(url, headers=header, verify=False)
        if res.status_code != 200:
            return {"code": 404, "errmsg": "页面爬取失败: {}".format(res.status_code)}
        html = res.content.decode()
        page = etree.HTML(html)
        try:
            if page.xpath('//*[@id="wrapper"]/div[1]/ul/li[1]/text()')[0] == '呃...你想要的页面不存在':
                return {"code": 404, "errmsg": "影片不存在"}
        except Exception as e:
            logger.info('电影页面存在, 继续爬取:{}'.format(e))
        first_name = page.xpath('//*[@id="content"]/h1/span[1]/text()')[0].strip()
        last_name = page.xpath('//*[@id="info"]/span[./text()="又名:"]/following::text()[1]')[0].strip()
        this_url = url
        img = page.xpath('//*[@id="mainpic"]/a/img/@src')[0]
        def_img = 'https://images.weserv.nl/?url=' + img
        data_dict = {
            "name": first_name + '/' + last_name,
            "url": this_url,
            "img": def_img,
        }
        print('------------爬虫结束-------------')
        print('爬取内容: {}'.format(data_dict))
    except Exception as e:
        logger.info('爬取失败: {}'.format(e))
        return {"code": 404, "errmsg": "爬取发生意外造成失败!"}
    try:
        # 如果json文件不存在, 会报错, 故此使用try
        with open(os.getcwd() + '/static/json/{}_movie.json'.format(status), 'r+') as json_file:
            open_file = json.load(json_file)
    except Exception as e:
        print('文件不存在: 设置open_file = {}')
        # 如果失败了, 给他设置为一个空字典, 最终以[编号: {剧1}, 编号: {剧2}, ...]方式写入
        open_file = {}
    try:
        open_file.setdefault(num, data_dict)
        with open(os.getcwd() + '/static/json/{}_movie.json'.format(status), 'w+') as json_file:
            json.dump(open_file, json_file)
    except Exception as e:
        print('电影写入失败: {}'.format(e), data_dict)
        logger.info('电影写入失败: {}'.format(e) )
        return {"code": 404, "errmsg": "电影写入失败!"}
    data = {
        'name': first_name,
        'num': num,
    }
    return data


def CrawlDBBook(value, sta):
    num = value
    status = sta
    if status not in ['wish', 'read']:
        return {"code": 404, "errmsg": "书籍分类不正确"}
    url = 'https://book.douban.com/subject/{}/'.format(num)
    urllib3.disable_warnings()
    try:
        # 构造爬虫, 爬取番剧数据
        print('------------爬虫开始-------------')
        res = requests.get(url, headers=header, verify=False)
        if res.status_code != 200:
            return {"code": 404, "errmsg": "页面爬取失败: {}".format(res.status_code)}
        html = res.content.decode()
        page = etree.HTML(html)
        try:
            if page.xpath('//*[@id="wrapper"]/div[1]/ul/li[1]/text()')[0] == '呃...你想要的页面不存在':
                return {"code": 404, "errmsg": "影片不存在"}
        except Exception as e:
            logger.info('书籍页面存在, 继续爬取:{}'.format(e))
        img = page.xpath('//*[@id="mainpic"]/a/img/@src')[0]
        def_img = 'https://images.weserv.nl/?url=' + img
        title = page.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
        rating = page.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
        try:
            author = "".join(page.xpath('//*[@id="info"]//span[./text()="作者:"]/following::a[1]/text()')[0].split())
        except Exception as e:
            logger.info('方案1失败, 使用方案2继续爬取:{}'.format(e))
            try:
                author = "".join(page.xpath('//*[@id="info"]//span[./text()=" 作者"]/following::a[1]/text()')[0].split())
            except Exception as e:
                logger.info('方案2失败, 使用方案2继续爬取:{}'.format(e))
                return {"code": 404, "errmsg": "书籍名称爬取失败"}
        summary = '\n'.join(page.xpath('//*[@id="link-report"]//div[@class="intro"]/p/text()'))
        data_dict = {
            'img': def_img,
            'title': title,
            'rating': rating,
            'author': author,
            'link': url,
            'summary': summary,
        }
        print('------------爬虫结束-------------')
        print('爬取内容: {}'.format(data_dict))
    except Exception as e:
        logger.info('爬取失败: {}'.format(e))
        return {"code": 404, "errmsg": "爬取失败!"}
    try:
        # 如果json文件不存在, 会报错, 故此使用try
        with open(os.getcwd() + '/static/json/{}_book.json'.format(status), 'r+') as json_file:
            open_file = json.load(json_file)
    except Exception as e:
        print('文件不存在: 设置open_file = {}')
        # 如果失败了, 给他设置为一个空字典, 最终以[编号: {剧1}, 编号: {剧2}, ...]方式写入
        open_file = {}
    try:
        open_file.setdefault(num, data_dict)
        with open(os.getcwd() + '/static/json/{}_book.json'.format(status), 'w+') as json_file:
            json.dump(open_file, json_file)
    except Exception as e:
        print('书籍写入失败: {}'.format(e), data_dict)
        logger.info('书籍写入失败: {}'.format(e))
        return {"code": 404, "errmsg": "书籍写入失败!"}
    data = {
        'name': title,
        'num': num,
    }
    return data
