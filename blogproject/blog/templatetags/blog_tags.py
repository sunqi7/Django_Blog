from ..models import Post, Category, Tags

# 导入template模块，然后实例化一个template.Library类，并将函数装饰为register.simple_Tag，这样就可以在模板中使用
# { % get_recent_posts() %}
from django import template

from django.db.models.aggregates import Count

register = template.Library()


# 最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-creatd_time')[:num]


# 分类模板标签
@register.simple_tag()
def get_categories():
    # 顶部引进category类
    # 顶部引入count函数
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # return Category.objects.all()

# 归档模板标签
@register.simple_tag()
def archives():
    '''
    这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 Python 的 date 对象，精确到月份，降序排列。
    接受的三个参数值表明了这些含义，一个是 created_time ，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。
    例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
    那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
    '''
    return Post.objects.dates('creatd_time', 'month', order='DESC')


@register.simple_tag()
def get_tags():
    return Tags.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
