from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    """
    模型必须继承models.Model类
    CharField是字符类型
    max_length指定最大长度

    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文，TextField可存储大段文本
    body = models.TextField()
    # 创建时间，DateTimeField类型
    create_time = models.DateTimeField()
    # 最后一次修改时间，DateTimeField类型
    modified_time = models.DateTimeField()
    # 文章摘要，blank=True，参数可以为空值
    excerpt = models.CharField(max_length=200, blank=True)
    """
    分类：一篇文章只能对应一个分类，一个分类下课有多篇文章
    分类已经定义，用ForeignKey表示一对多的关系
    """
    category = models.ForeignKey(Category)
    """
    标签：一篇文章可以有多篇文章，一篇文章有多个标签
    ManyToManyField多对多的关联关系
    """
    tags = models.ManyToManyField(Tag, blank=True)
    """
    作者：User是从django.contrib.auth.models导入的
    django.contrib.auth是django的内置应用，专门用于处理网站用户的注册，登录等流程
    一篇文章只能有一个作者，一个作者可能会写多篇文章
    """
    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            self.excerpt = strip_tags(md.convert(self.body))[:200]
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-create_time']
