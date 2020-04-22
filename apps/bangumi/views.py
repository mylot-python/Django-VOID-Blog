import json, os, logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from articles.models import Category

logger = logging.getLogger('django')


class BangumiPage(View):
    """
    追番页面
    route: /bangumi/
    """
    def get(self, request):
        context = {
            'cls': Category.objects.all(),
        }
        return render(request, 'share/bangumi.html', context=context)


class BangumiJson(View):
    """
    追番json获取
    route: /bangumi/json/
    """

    def get(self, request):
        try:
            form = int(request.GET.get('from', 0))
        except Exception as e:
            logger.info('请求参数有误: {}'.format(e))
            return JsonResponse({}, safe=False)

        try:
            with open(os.getcwd() + '/static/json/bangumi_dict.json', 'r') as file:
                json_data = json.load(file)
                length = 9
                data = []
                data_len = len(json_data.values())
                data_list =  list(json_data.values())
                data_list.reverse()
                if form < data_len:
                    length = length + form
                    data = data_list[form: length]
                    # 解决跨域问题
                    # res = HttpResponse(json.dumps(data))
                    # # obj['Access-Control-Allow-Origin']='*'
                    # res['Access-Control-Allow-Origin'] = '地址'
                    # return res
                    return JsonResponse(data, safe=False)
                else:
                    # 解决跨域问题
                    # res = HttpResponse(json.dumps(data))
                    # # obj['Access-Control-Allow-Origin']='*'
                    # res['Access-Control-Allow-Origin'] = '地址'
                    # return res
                    return JsonResponse(data, safe=False)
        except Exception as e:
            logger.info('获取bangumi_dict.json失败: {}'.format(e))
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = '地址'
            # return res
            return JsonResponse({}, safe=False)