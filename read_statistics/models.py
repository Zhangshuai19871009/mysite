from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone

# 记录阅读数量
class ReadNum(models.Model):
    # 阅读数
    read_num = models.IntegerField(verbose_name='阅读总数', default=0)

    # 建立对应模型外键
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 对应模型主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读总数'
        verbose_name_plural = verbose_name

# 获取阅读数量的公共方法
class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

# 记录详细阅读信息
class ReadDetail(models.Model):
    # 阅读日期
    date = models.DateField(verbose_name='阅读日期', default=timezone.now)
    read_num = models.IntegerField(verbose_name='阅读数', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读信息'
        verbose_name_plural = verbose_name
