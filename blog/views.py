from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read

# 获取博客列表共同的数据
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 没页显示条数
    page_num = request.GET.get('page', 1)  # 获取url的页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页的前后两页，max(current_page_num-2, 1)表示当前页前两页跟1比较取最大值，避免得到小于1的页码
    # min(current_page_num+2, paginator.num_pages)表示最大页跟当前页后两页比较取最小值，避免超出页码范围，
    # +1表示range右边是开区间，取不到值
    page_range = [i for i in range(max(current_page_num - 2, 1), min(current_page_num + 2, paginator.num_pages) + 1)]
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应的博客数量
    blog_type_list = BlogType.objects.annotate(blog_count=Count('blog'))
    '''
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    # 需要查找的所有博客信息
    context['blogs'] = page_of_blogs.object_list
    # 分页显示的博客信息
    context['page_of_blogs'] = page_of_blogs
    # 分页页码
    context['page_range'] = page_range
    # 博客类型分类
    context['blog_types'] = blog_type_list
    # 博客日期分类
    context['blog_dates'] = blog_dates_dict
    return context

# 博客列表页
def blog_list(request):
    # 获取所有的博客文章
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

# 博客分类页
def blogs_with_type(request, blog_type_pk):
    # 获取博客类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 根据博客类型获取博客文章
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    # 博客类型
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

# 博客按月分类
def blogs_with_date(request, year, month):
    # 根据博客日期获取博客文章
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    # 博客日期
    context['blogs_with_date'] = '{0}年{1}月'.format(year, month)
    return render(request, 'blog/blogs_with_date.html', context)

# 博客详情页
def blog_deltail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    # 上一篇博客信息
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 当前博客信息
    context['blog'] = blog
    # 下一篇博客信息
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    # 响应
    response = render(request, 'blog/blog_detail.html', context)
    # 阅读cookie标记
    response.set_cookie(read_cookie_key, 'true')
    return response
