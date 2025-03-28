from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

@login_required #로그인 안 하면 create로 못감
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)





def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'detail.html', context)

@login_required
def comment_create(request, article_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        
        # # 객체를 저장하는 경우
        # comment.user = request.user
        # article = Article.objects.get(id=article_id)
        # comment.article = article

        # id값을 저장하는 경우
        comment.user_id = request.user.id
        comment.article_id = article_id

        
        comment.save()

        return redirect('articles:detail', id=article_id)