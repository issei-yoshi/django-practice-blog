from django.db import models

class Category(models.Model):
    name = models.CharField("カテゴリー", max_length=255)
    slug = models.SlugField(unique=True)

class Post(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    is_published = models.BooleanField("公開設定", default=False)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title