import json, os, logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from articles.models import Category

logger = logging.getLogger('django')


class MoviePage(View):
    """
    观影页面
    route: /movie/
    """
    def get(self, request):
        context = {
            'cls': Category.objects.all(),
        }
        return render(request, 'share/movie.html', context=context)


class MovieJson(View):
    """
    观影json
    route: /movie/json/
    """

    def get(self, request):
        try:
            form = int(request.GET.get('from'))
            status = request.GET.get('status')
        except Exception as e:
            logger.info('请求参数有误: {}'.format(e))
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = '地址'
            # return res
            return JsonResponse({}, safe=False)

        if not status or status not in ['wish', 'watched']:
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = '地址'
            # return res
            return JsonResponse({}, safe=False)
        try:
            with open(os.getcwd() + '/static/json/{}_movie.json'.format(status), 'r') as file:
                json_data = json.load(file)
                length = 4
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
                    # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
                    # return res
                    return JsonResponse(data, safe=False)
                else:
                    # 解决跨域问题
                    # res = HttpResponse(json.dumps(data))
                    # # obj['Access-Control-Allow-Origin']='*'
                    # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
                    # return res
                    return JsonResponse(data, safe=False)
        except Exception as e:
            logger.info('获取{}_movie.json失败: {}'.format(status, e))
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
            # return res
            return JsonResponse({}, safe=False)


