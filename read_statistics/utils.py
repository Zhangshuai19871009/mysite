import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{0}_{1}_read".format(ct.model, obj.pk)

    if not request.COOKIES.get(key):
        ct = ContentType.objects.get_for_model(obj)
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在对应的记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)

        # 总阅读数 +1, get_or_create如果不存在就创建，等同与上面注释掉的代码
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读量 +1
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=timezone.now().date())
        # 增加阅读量
        readDetail.read_num += 1
        readDetail.save()
    return key

# 获取前七天阅读量方法
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, dates

# 当天热门博客排行榜
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects\
        .filter(content_type=content_type, date=today)\
        .order_by('-read_num')
    return read_details[:7]

# 昨天热门博客排行榜
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects\
        .filter(content_type=content_type, date=yesterday)\
        .order_by('-read_num')
    return read_details[:7]
