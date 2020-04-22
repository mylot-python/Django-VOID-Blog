import random

from django.shortcuts import render
from django.views import View

from articles.models import Category
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