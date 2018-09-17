from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogUser
from .utils import *
from .forms import *


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_delete_form.html'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_delete_form.html'
    raise_exception = True


class UserCreate(ObjectCreateMixin, View):
    model = BlogUser
    model_form = UserForm
    template = 'blog/user_sign_up_form.html'


class UserDetail(View):

    def get(self, request, id):
        obj = get_object_or_404(BlogUser, id=id)
        return render(request, 'blog/user_detail.html', context={
            'user': obj,
            'admin_object': obj,
            'detail': True}
                      )


def posts_list(request):
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 3)

    page = paginator.get_page(page_number)
    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''
    is_paginated = page.has_other_pages()

    context = {
        'page_object': page,
        'prev_url': prev_url,
        'next_url': next_url,
        'is_paginated': is_paginated
    }

    return render(request, 'blog/index.html', context=context)


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'blog/user_sign_in_form.html')
    else:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts_list_url')
        else:
            return render(request, 'blog/user_sign_in_form.html')


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


def users_list(request):
    users = BlogUser.objects.all()
    return render(request, 'blog/users_list.html', context={'users': users})
