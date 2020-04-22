import json, os, logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.CrawlDB import CrawlDBMovie
from .models import MovieModel


@receiver(post_save, sender=MovieModel)
def movie_write_json(sender, instance=None, created=False, **kwargs):
    logger = logging.getLogger('django')
    num = str(instance.num)
    status = instance.status
    new_status = 'watched' if  status == 1 else 'wish'
    original_status = 'wish' if status == 1 else 'watched'
    if created:
        CrawlDBMovie(num, new_status)
        print('新增成功')
    else:
        try:
            # 如果json文件不存在, 会报错, 故此使用try
            # 打开原分类所在json
            with open(os.getcwd() + '/static/json/{}_movie.json'.format(original_status), 'r') as json_file:
                original_file = json.load(json_file)
                original = original_file.get(num)
            # 打开新分类所在json
            with open(os.getcwd() + '/static/json/{}_movie.json'.format(new_status), 'r') as json_file:
                change_file = json.load(json_file)
                change_file.setdefault(num, original)
            del original_file[num]
            with open(os.getcwd() + '/static/json/{}_movie.json'.format(original_status), 'w') as json_file:
                json.dump(original_file, json_file)
            with open(os.getcwd() + '/static/json/{}_movie.json'.format(new_status), 'w') as json_file:
                json.dump(change_file, json_file)
        except Exception as e:
            logger.error('movie_write_json引发错误: ', e)




