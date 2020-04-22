from datetime import datetime
from django.db import models


class LinksModel(models.Model):
    """
    友链模型
    """

    BIG_OR_SMALL = (
        [0, '是个小伙伴'],
        [1, '是个大佬'],
    )

    name = models.CharField(verbose_name='伙伴名', max_length=64)
    site_name = models.CharField(verbose_name='站点名', max_length=64, null=True)
    site_url = models.URLField(verbose_name='站点url')
    image_url = models.URLField(verbose_name='站点头像url')
    status = models.IntegerField(verbose_name='大佬或小伙伴', choices=BIG_OR_SMALL, default=0)
    text = models.TextField('备注', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'tb_links'
        verbose_name = '友链'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name