import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# 多线程异步发送邮件
class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            self.fail_silently,
            html_message=self.text
        )

# 评论
class Comment(models.Model):
    # 建立对应模型外键
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 对应模型主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论/回复内容')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    # related_name='comments' 给外键添加别名，
    # 用于区别引用同一个模型对象时产生的异常
    user = models.ForeignKey(User, verbose_name='评论/回复人', related_name='comments', on_delete=models.CASCADE)

    # 记录每一条评论的顶级
    root = models.ForeignKey("self", verbose_name='顶级评论', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 父级id，通过外键添加并关联回复对象,反向关联到自身
    parent = models.ForeignKey('self', verbose_name='父级评论', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def send_mail(self):
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客' # 主题
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'  # 主题
            email = self.reply_to.email

        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_email.html', context)
            send_email = SendMail(subject, text, email)
            send_email.start()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['comment_time']
