import json, logging, os

from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.CrawlDB import CrawlDBBook
from .models import BookModel


logger = logging.getLogger('django')

@receiver(post_save, sender=BookModel)
def book_write_json(sender, instance=None, created=False, **kwargs):
    num = str(instance.num)
    status = instance.status
    new_status = 'read' if  status == 1 else 'wish'
    original_status = 'wish' if status == 1 else 'read'
    if created:
        CrawlDBBook(num, new_status)
        print('新增成功')
    else:
        try:
            # 如果json文件不存在, 会报错, 故此使用try
            # 打开原分类所在json
            with open(os.getcwd() + '/static/json/{}_book.json'.format(original_status), 'r') as json_file:
                original_file = json.load(json_file)
                original = original_file.get(num)
            # 打开新分类所在json
            with open(os.getcwd() + '/static/json/{}_book.json'.format(new_status), 'r') as json_file:
                change_file = json.load(json_file)
                change_file.setdefault(num, original)
            del original_file[num]
            with open(os.getcwd() + '/static/json/{}_book.json'.format(original_status), 'w') as json_file:
                json.dump(original_file, json_file)
            with open(os.getcwd() + '/static/json/{}_book.json'.format(new_status), 'w') as json_file:
                json.dump(change_file, json_file)
        except Exception as e:
            logger.error('book_write_json引发错误: ', e)