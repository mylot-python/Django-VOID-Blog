import json, os, logging, requests
from lxml import etree


def CrawlBangumi(num):
    logger = logging.getLogger('django')

    header = {
        'Referer': 'https://www.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    url = 'http://bgm.tv/subject/{}'.format(num)

    try:
        # 构造爬虫, 爬取番剧数据
        print('------------爬虫开始-------------')
        res = requests.get(url, headers=header, verify=False)
        html = res.content.decode()
        page = etree.HTML(html)
        if res.status_code != 200:
            return None

        # 这个try是防止code200返回的是网站自定义的404页面
        try:
            if page.xpath('//*[@id="colunmNotice"]/div/h2/text()')[0] == '呜咕，出错了':
                return None
        except Exception as e:
            logger.info('番号页面存在, 继续爬取, 页面出错检测:{} 成功'.format(e))

        # 这个try的连用是来抓取集数的, 由于动漫版块和电视剧版块结构不一样, 使用3个try
        # try1是针对动漫抓取的, try2是针对电视剧抓取的
        # try3是通用抓取的li个数统计集数的, 动漫和电视剧都有, 所以放在后面, 应该不会报错
        try:
            count = int(page.xpath('//*[@id="infobox"]/li/span[text()="话数: "]/following::text()[1]')[0])
        except Exception as e:
            logger.info('番号集数采取失败, 使用二套方案, 继续爬取:{}'.format(e))
            try:
                count = int(page.xpath('//*[@id="infobox"]/li/span[text()="集数: "]/following::text()[1]')[0])
            except Exception as e:
                logger.info('番号集数采取失败, 使用第三套方案, 继续爬取:{}'.format(e))
                count = len(page.xpath('//*[@id="subject_detail"]/div[1]/ul/li[not(@class="subtitle")]'))

        # 这个try是用来抓取开播日期的
        try:
            air_date = page.xpath('//*[@id="infobox"]/li/span[text()="放送开始: "]/following::text()[1]')[0]
        except Exception as e:
            logger.info('开播日期采取失败, 使用二套方案, 继续爬取:{}'.format(e))
            try:
                air_date = page.xpath('//*[@id="infobox"]/li/span[text()="开始: "]/following::text()[1]')[0]
            except Exception as e:
                logger.info('开播日期二套方案也失败了!: {}'.format(e))
                return None

        # 这个try是用来抓取放送日期的
        try:
            air_weekday = page.xpath('//*[@id="infobox"]/li/span[text()="放送星期: "]/following::text()[1]')[0]
        except Exception as e:
            logger.info('放送日期采取失败, 使用二套方案, 继续爬取:{}'.format(e))
            try:
                air_weekday = page.xpath('//*[@id="infobox"]/li/span[text()="开始: "]/following::text()[1]')[0]
            except Exception as e:
                logger.info('放送日期二套方案也失败了!: {}'.format(e))
                return None

        # 构造dict, 这些不会出错的爬取就没有使用try, 直接写入字典
        data_dict = {
            "name": page.xpath('//*[@id="headerSubject"]/h1/a/text()')[0],
            "name_cn": page.xpath('//*[@id="infobox"]/li[1]/text()')[0],
            "url": url,
            "status": 0,
            "count": count,
            "air_date": air_date,
            "air_weekday": air_weekday,
            "img": page.xpath('//*[@id="bangumiInfo"]/div/div/a/@href')[0],
            "id": num
        }

        print('------------爬虫结束-------------')
        print('爬取内容: {}'.format(data_dict))
    except Exception as e:
        logger.info('爬取失败: {}'.format(e))
        return None

    try:
        # 如果json文件不存在, 会报错, 故此使用try
        with open(os.getcwd() + '/static/json/bangumi_dict.json', 'r') as json_file:
            open_file = json.load(json_file)
    except Exception as e:
        print('文件不存在: 设置open_file = {}')
        # 如果失败了, 给他设置为一个空字典, 最终以[编号: {番剧1}, 编号: {番剧2}, ...]方式写入
        open_file = {}

    try:
        # 如果以上正确运行, 则直接写入新加的番剧
        open_file.setdefault(num, data_dict)
        with open(os.getcwd() + '/static/json/bangumi_dict.json', 'w') as json_file:
            json.dump(open_file, json_file)
    except Exception as e:
        print('番剧写入失败: {}'.format(e), data_dict)
        logger.info('番剧写入失败: {}'.format(e))
        return None

    return data_dict