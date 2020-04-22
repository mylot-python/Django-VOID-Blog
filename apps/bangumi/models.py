from datetime import datetime
from django.db import models


class BangumiModel(models.Model):
    """
    追番模型
    """
    name = models.CharField(verbose_name='番名', max_length=64, null=True, blank=True)
    num = models.IntegerField(verbose_name='番号id')
    status = models.IntegerField(verbose_name='已看数', default=0, null=True, blank=True)
    count = models.IntegerField(verbose_name='总集数', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_bangumi'
        verbose_name = '追番'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name