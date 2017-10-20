from django.shortcuts import render, get_object_or_404
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Category, Tags
from comments.forms import CommentForm

# 引入Markdown模块
'''
Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，Markdown 的渲染器就能够把我们写的文章转换为标准的 HTML 文档，
从而让我们的文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。由于 Markdown 语法简单直观
'''
import markdown


# 主页视图
def index(request):
    post_list = Post.objects.all().order_by('-creatd_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


# 详情页视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 评论数+1
    post.increase_views()

    # 文章内容进行markdown处理
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

    form = CommentForm()
    # 获取这篇Post下所有评论
    comment_list = post.comment_set.all()
    for cl in comment_list:
        cl.text = markdown.markdown(cl.text, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])




    # 将文章、表单以及文章下的评论列表作为模板变量传给detail.html模板，以便渲染相应数据
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'blog/detail.html', context=context)


# 归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(
        creatd_time__year=year,
        creatd_time__month=month,
    ).order_by(
        '-creatd_time'
    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类页视图
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(categoty=cate).order_by('-creatd_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 标签页视图
def tags(request, pk):
    tag = get_object_or_404(Tags, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-creatd_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
