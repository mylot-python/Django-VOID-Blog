import json, logging, os
from django.db.models.signals import post_save
from django.dispatch import receiver


from utils.CrawlBangumi import CrawlBangumi
from .models import BangumiModel





@receiver(post_save, sender=BangumiModel)
def bangumi_write_json(sender, instance=None, created=False, **kwargs):
    logger = logging.getLogger('django')
    num = str(instance.num)
    if created:
        res = CrawlBangumi(num)
        if res:
            instance.name = res['name_cn']
            instance.count = res['count']
            instance.save()
    else:
        status = instance.status
        try:
            # 如果json文件不存在, 会报错, 故此使用try
            with open(os.getcwd() + '/static/json/bangumi_dict.json', 'r') as json_file:
                open_file = json.load(json_file)
                change = open_file.get(num)
                if not change:
                    return
                if status > change['count'] or status == change['status']:
                    return
                logger.info('-----修改前进度-----: {}'.format(change['status']))
                change['status'] = status
                open_file.setdefault(num, change)
                logger.info('-----修改后进度-----: {}'.format(open_file.get(num)['status']))
            # 如果以上正确运行, 则把更新好的json数据重新写入
            with open(os.getcwd() + '/static/json/bangumi_dict.json', 'w') as json_file:
                json.dump(open_file, json_file)
                logger.info('-----进度修改成功-----')
        except Exception as e:
            logger.info('打开文件或写入失败: {}'.format(e))
            return

