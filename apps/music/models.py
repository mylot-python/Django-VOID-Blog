from datetime import datetime
from django.db import models


class MusicModel(models.Model):
    """
    音乐模型
    """

    list_num = models.IntegerField(verbose_name='歌单编号')
    server = models.CharField(verbose_name='歌单服务商', max_length=12)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_music'
        verbose_name = '音乐'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.list_num)