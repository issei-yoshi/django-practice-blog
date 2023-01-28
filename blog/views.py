from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView

from blog.models import Post, Category, Tag, Comment, Reply
from blog.forms import CommentForm, ReplyForm

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    # paginate_by = 1

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
    context_object_name = "posts" #デフォルトではpost_listとなっているものをpostsに変更している
    paginate_by = 1

    def get_queryset(self):
        #TOPページでアクセスのあったカテゴリーのURLをslugに代入
        slug = self.kwargs["slug"]
        #カテゴリーが存在したら代入、存在しなかったら404エラーを返す
        self.category = get_object_or_404(Category, slug=slug)
        #filterを使って取得した記事からカテゴリーごとに絞り込み
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs) #object_listなど色々格納されている
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        slug = self.kwargs["slug"]
        self.tag = get_object_or_404(Tag, slug=slug)
        return super().get_queryset().filter(tag=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class SearchPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        self.query = self.request.GET.get('query') or "" #フォームで送信されたキーワードを取得する, queryはフォームで設定する
        #requestはHttpリクエストが送られたときにDjangoが作るオブジェクト
        #request.GETを実行するとrequestの情報を辞書型のデータで取得できる
        #getメソッドを実行すると辞書型のオブジェクトからキーを指定して値を取得できる
        queryset = super().get_queryset()

        if self.query:
            queryset = queryset.filter(
                #titleがqueryを含んでいるまたはcontentがqueryを含んでいる場合
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        self.post_count = len(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        context["post_count"] = self.post_count
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form): #フォームで送られてきた内容を変更する
        comment = form.save(commit=False) #フォームから送られてきた内容を保存する前にform_validメソッド内で使えるようになる
        post_pk = self.kwargs['post_pk'] #記事のpkを取得して代入しておく
        post = get_object_or_404(Post, pk=post_pk) #Postが存在するかどうかを判定
        comment.post = post
        comment.save()
        return redirect('post-detail', pk=post_pk)

    def get_context_data(self, **kwargs): #コメントを投稿するページにて記事の内容も出しておく #記事の情報もテンプレートに渡す
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['post_pk'] #コメントのkwargsからpost_pkを取得
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context


class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form): #フォームで送られてきた内容を変更する
        reply = form.save(commit=False) #フォームから送られてきた内容を保存する前にform_validメソッド内で使えるようになる
        comment_pk = self.kwargs['comment_pk'] #コメントのpkを取得して代入しておく
        comment = get_object_or_404(Comment, pk=comment_pk) #Commentが存在するかどうかを判定
        reply.comment = comment
        reply.save()
        return redirect('post-detail', pk=comment.post.pk)

    def get_context_data(self, **kwargs): #コメントを投稿するページにて記事の内容も出しておく #記事の情報もテンプレートに渡す
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['comment_pk'] #コメントのkwargsからcomment_pkを取得
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context