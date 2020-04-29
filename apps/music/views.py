import requests, random, os, json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from articles.models import Category
from utils.CrawlMusic import CrawlAPI
from .models import MusicModel

class MusicPage(View):
    """
    音乐页面
    route: /music/
    """

    def get(self, request):
        musics = MusicModel.objects.all()
        if musics:
            music = random.choice(musics)
            list_num = music.list_num
            server = music.server
            context = {
                'list_num': list_num,
                'server': server,
                'cls': Category.objects.all(),
            }
        else:
            context = {}
        return render(request, 'share/music.html', context=context)


class MusicApi(View):

    def get(self, request):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        api = 'https://api.i-meto.com/meting/api?server={}&type={}&id={}&auth={}&r={}'
        server = request.GET.get('server')
        type = request.GET.get('type')
        id = request.GET.get('id')
        auth = request.GET.get('auth', None)
        r = request.GET.get('r', None)

        if type == 'playlist':
            try:
                with open(os.getcwd() + '/static/json/music_api_{}.json'.format(id), 'r') as f:
                    open_file = f.read()
                    # 由于歌单会更新, 本来我站点里这里是配置的异步的,
                    # 但是考虑到还要安装celery, 这里就直接调用一下
                    CrawlAPI(server, type, id, auth, r)
                    return HttpResponse(open_file)
            except Exception as e:
                print(e)
            # 如果json文件不存在, 则爬取data
            data = CrawlAPI(server, type, id, auth, r)
            return HttpResponse(json.dumps(data))
        elif type == 'lrc':
            res = requests.get(api.format(server, type, id, auth, r), headers=header, verify=False)
            html = """<pre style="word-wrap: break-word; white-space: pre-wrap;">"{}"</pre>""".format(res.text)
            return HttpResponse(html)
        elif type == 'pic':
            res = requests.get(api.format(server, type, id, auth, r), headers=header, verify=False)
            return HttpResponse(res.content)
        elif type == 'url':
            res = requests.get(api.format(server, type, id, auth, r), headers=header, verify=False)
            return HttpResponseRedirect(res.url)
        else:
            return HttpResponse({})