from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import PostSerializer
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

class IntruderImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@csrf_exempt  # CSRF 보안 예외 처리 (테스트 목적으로)
def post_data(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        created_date = request.POST.get('created_date')
        published_date = request.POST.get('published_date')

        # 데이터베이스에 저장 (모델과 필드 이름을 실제 데이터 모델에 맞게 수정)
        Post.objects.create(title=title, text=text, created_date=created_date, published_date=published_date)

        return JsonResponse({'message': 'Data posted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)