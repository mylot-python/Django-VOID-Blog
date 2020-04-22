import json, logging, os

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from articles.models import Category


logger = logging.getLogger('django')


class BookPage(View):
    """
    阅读页面
    route: /book/
    """

    def get(self, request):
        context = {
            'cls': Category.objects.all(),
        }
        return render(request, 'share/book.html', context=context)


class BookJson(View):
    """
    阅读json
    route: /book/json/
    """

    def get(self, request):
        try:
            form = int(request.GET.get('from', 0))
            status = request.GET.get('status')
        except Exception as e:
            logger.info('请求参数有误: {}'.format(e))
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
            # return res
            return JsonResponse({}, safe=False)
        if not status or status not in ['wish', 'read']:
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
            # return res
            return JsonResponse({}, safe=False)
        try:
            with open(os.getcwd() + '/static/json/{}_book.json'.format(status), 'r') as file:
                json_data = json.load(file)
                length = 4
                data = []
                data_len = len(json_data.values())
                data_list =  list(json_data.values())
                data_list.reverse()
                print(form)
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
            logger.info('获取{}_book.json失败: {}'.format(status, e))
            # 解决跨域问题
            # res = HttpResponse(json.dumps({}))
            # # obj['Access-Control-Allow-Origin']='*'
            # res['Access-Control-Allow-Origin'] = 'http://139.9.5.228:9999'
            # return res
            return JsonResponse({}, safe=False)

