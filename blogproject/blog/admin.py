from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tags


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'creatd_time', 'modfied_time', 'categoty', 'author']


# 把新增的postadmin也注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tags)
