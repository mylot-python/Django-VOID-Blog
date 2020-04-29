import json, logging, requests, os

logger = logging.getLogger('django')

def CrawlAPI(server, type, id, auth, r):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    api = 'https://api.i-meto.com/meting/api?server={}&type={}&id={}&auth={}&r={}'
    url = api.format(server, type, id, auth, r)
    res = requests.get(url, headers=header)
    if res.status_code == 200:
        data = res.json()
        if len(data) != 0:
            try:
                for i in data:
                    i['url'] = i['url'].replace('https://api.i-meto.com/meting/api',
                                                'http://127.0.0.1:8000/music/api/')
                    i['cover'] = i['cover'].replace('https://api.i-meto.com/meting/api',
                                                    'http://127.0.0.1:8000/music/api/')
                    i['lrc'] = i['lrc'].replace('https://api.i-meto.com/meting/api',
                                                'http://127.0.0.1:8000/music/api/')
                with open(os.getcwd() + '/static/json/music_api_{}.json'.format(id), 'w+') as f:
                    json.dump(data, f)
                return data
            except Exception as e:
                logger.info('music_api写入失败: {}'.format(e))
            return data
    else:
        logger.info('requests获取失败')
        return []


