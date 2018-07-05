from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BlogType(models.Model):
    type_name = models.CharField(verbose_name='类型', max_length=15)

    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(verbose_name='标题', max_length=50)
    # 博客类型一种博客一种类型
    blog_type = models.ForeignKey(BlogType, verbose_name='类型', on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='博客内容')
    # 作者 通过外键关联到系统用户表
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    # 反向泛型关系,可以访问到ReadDetail的数据
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    last_updated_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    # 通过对象反向解析，获取url连接
    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    # 获取当前用户的email
    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
