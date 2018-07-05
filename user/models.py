from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户名')
    nickname = models.CharField(verbose_name='昵称' ,max_length=20)

    def __str__(self):
        return '<Profile: {0} for {1}>'.format(self.nickname, self.user.username)

    class Meta:
        verbose_name = '用户拓展'
        verbose_name_plural = verbose_name

# 动态绑定昵称
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

# 获取昵称或者用户名
def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

# 是否有昵称
def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
