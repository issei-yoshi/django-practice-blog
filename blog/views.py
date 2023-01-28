from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView

from blog.models import Post, Category

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        posts = super().get_queryset() #querysetには全ての記事が格納されている
        return posts.order_by('-updated_at')


class PostDetailView(DeleteView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_object(self, queryset=None):
        post = super().get_object(queryset) #ここで詳細記事を返している
        if post.is_published or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        #TOPページでアクセスのあったカテゴリーのURLをslugに代入
        slug = self.kwargs["slug"]
        #カテゴリーが存在したら代入、存在しなかったら404エラーを返す
        self.category = get_object_or_404(Category, slug=slug)
        #filterを使って取得した記事からカテゴリーごとに絞り込み
        return super().get_queryset().filter(category=self.category)