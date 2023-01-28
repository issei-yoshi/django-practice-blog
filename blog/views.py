from django.shortcuts import render
from django.views.generic import ListView, DeleteView

from blog.models import Post

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

class PostDetailsView(DeleteView):
    model = Post
    template_name = "blog/post_detail.html"