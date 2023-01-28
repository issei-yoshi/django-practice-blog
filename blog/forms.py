from django import forms
from blog.models import Comment, Reply

class CommentForm(forms.ModelForm):
    model = Comment
    fields = ("name", "text")
    widgets = {
        'name': forms.TextInput(attrs={'placeholder': '名前'}),
        'text': forms.Textarea(attrs={'placeholder': 'コメントを入力してください。'})
    }