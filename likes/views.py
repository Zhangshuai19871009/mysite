from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

# 返回错误信息
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

# 返回成功数据
def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(4000, '没有登录，不能点赞')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(4000, '对象不存在')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        # 获取不到就创建
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(4001, '你已经点赞过')
    else:
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数 -1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(4003, '数据错误')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(4002, '你没有点赞过，不能取消')

