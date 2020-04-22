from datetime import datetime
from django.db import models


class BookModel(models.Model):
    """
    create book model
    """
    STATUS_CHOICES = (
        [0, 'wish'],
        [1, 'read'],
    )

    name = models.CharField(verbose_name='书名', max_length=64)
    num = models.IntegerField(verbose_name='书ID')
    status = models.SmallIntegerField(verbose_name='想看/已看', choices=STATUS_CHOICES, null=True, blank=True, default=0)
    create_time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_book'
        verbose_name = '读书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name