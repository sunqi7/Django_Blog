from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.
'''
分类
'''


class Category(models.Model):
    '''
    Django要求模型必须继承models.Model类。
    Categoty只需要一个简单的分类名name就可以了
    Charfield制定了分类名name的数据类型，Charfield是字符类型
    Charfield的max_lengh参数指定了其最大的长度，超过这个长度的分类名不能被存入数据库
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_category_url(self):
        return reverse('blog:Category', kwargs={'pk': self.pk})


'''
标签
'''


class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_tag_url(self):
        return reverse('blog:tag', kwargs={'pk': self.pk})


'''
文章
'''


class Post(models.Model):
    title = models.CharField(max_length=70)

    # 文章正文，我们使用TextField。
    # 存储短比较短的内容我们可以用CharField，但对于比较长的内容我们应该用TextField
    body = models.TextField()

    # 这两个列表示文章的创建时间和修改时间，存储时间用DateTimeField类型
    creatd_time = models.DateTimeField()
    modfied_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下，CharField要求我们必须存入数据，不然会报错
    # 指定Charfield的blank = True 参数值后就允许空值了
    excerpt = models.CharField(max_length=200, blank=True)

    # 分类和标签，分类和标签的模型在下面另外定义。
    # 我们要在这里把文章对应的数据库和分类，标签对应的数据库关联了起来，但是关联的形式稍微有点不同
    # 我们规定一篇文章只有一个分类，但是一个分类下面有多篇文章，所有我们使用的是ForeignKey，即一对多的关联方式
    # 而对标签来说，一篇文章可以有多个标签，同一个标签下面也有多个文章，所有我们使用的是ManyToManyField，表明这个是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此标签tags，指定了blank=True
    categoty = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags, blank=True)

    # 文章作者
    # django.contrib.auth是Django内置的应用，专门用于处理网站用户的登录注册等流程，User是Django为我们写好的用户模型。
    # 这里我们用ForeignKey把文章和User关联起来
    # 因为我们规定一篇文章只有一个作者，而一个作者可能有多篇文章，因此这个是一对多的关联关系。
    author = models.ForeignKey(User)

    # 阅读数
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def get_archives_url(self):
        return reverse('blog:archives', kwargs={'year': self.creatd_time.year, 'month': self.creatd_time.month})
        # { % url'blog:archives' date.year date.month %}

    class Meta:
        ordering = ['creatd_time', 'title']

    # 统计阅读数
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写save方法，为了从正文字段摘取前N个字符保存到摘要字段。
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先渲染一个Markdown类，用于渲染body文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            # 先将Markdown文本渲染成HTML文本
            # strip_tags去掉HTML文本的全部HTML标签
            # 从文本前摘取前54个字符赋给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)
