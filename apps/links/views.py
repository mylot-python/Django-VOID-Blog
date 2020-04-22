from django.shortcuts import render
from django.views import View

from .import models



class LinksPage(View):

    def get(self, request):

        friend = models.LinksModel.objects.only('name', 'image_url', 'site_url', 'status')
        big = friend.filter(status=1)
        small = friend.filter(status=0)

        context = {
            'big': big,
            'small': small,
        }
        return render(request, 'share/links.html', context=context)