from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Hashtag, Comment
from posts.forms import PostCreateForm, CommentCreateForm, HashtagCraeteForm
from users.utils import get_user_from_request

PAGINATION_LIMIT = 4


# Create your views here.
def posts_view(request):
    if request.method == 'GET':
        hashtag_id = request.GET.get('hashtag_id')
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()

        if search_text:
            posts = posts.filter(title__icontains=search_text)
        max_page = round(posts.__len__() / PAGINATION_LIMIT)
        posts = posts[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
        context = {
            'posts': posts,
            'user': get_user_from_request(request),
            'hastag_id': hashtag_id,
            'max_page': range(1, max_page + 1)
        }
        return render(request, 'posts/posts.html', context=context)


def hashtags_view(request, **kwargs):
    if request.method == 'GET':
        context = {
            'hashtags': Hashtag.objects.all(),
            'user': get_user_from_request(request)
        }
        return render(request, 'posts/hashtags.html', context=context)


def detail_view(request, **kwargs):
    if request.method == 'GET':
        post = Post.objects.get(id=kwargs['id'])
        print(post.title)
        data = {
            'post': post,
            'comments': Comment.objects.filter(id=kwargs['id']),
            'form': CommentCreateForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'posts/detail.html', context=data)

    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                author_id=1,
                text=form.cleaned_data.get('text'),
                post_id=kwargs['id']
            )
            post = Post.objects.get(id=kwargs['id'])
            data = {
                'post': post,
                'comments': Comment.objects.filter(post_id=kwargs['id']),
                'form': CommentCreateForm,
                'user': get_user_from_request(request)
            }
            return render(request, 'posts/detail.html', context=data)

        else:
            post = Post.objects.get(id=kwargs['id'])
            comment = Comment.objects.filter(post_id=post)
            data = {
                'post': post,
                'comments': comment,
                'form': CommentCreateForm,
                'user': get_user_from_request(request)
            }
            return render(request, 'posts/detail.html', context=data)


def posts_create_view(request):
    if request.method == 'GET':
        data = {
            'form': PostCreateForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'posts/create_post.html', context=data)
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                # photo=form.cleaned_data.get('photo'),
                likes=form.cleaned_data.get('likes'),
                hashtag=form.cleaned_data.get('hashtag')
            )
            return redirect('/posts')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)

            }
            return render(request, 'posts/create_post.html', context=data)

# def hashtags_create_view(request):
#     if request.method == 'GET':
#         data = {
#             'form': HashtagCraeteForm,
#             'user': get_user_from_request(request)
#
#         }
#         return render(request, 'posts/create_hashtag.html', context=data)
#     elif request.method == 'POST':
#         form = HashtagCraeteForm(data=request.POST)
#         if form.is_valid():
#             Hashtag.objects.create(
#                 title=form.cleaned_data.get('title')
#             )
#             return redirect('/hashtags/')
#         else:
#             data = {
#                 'form': form
#             }
#             return render(request, 'posts/create_hashtag.html', context=data)
