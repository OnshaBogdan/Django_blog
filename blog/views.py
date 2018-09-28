from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

import blog
from .models import BlogUser
from .utils import *
from .forms import *


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        current_user = BlogUser.objects.get(username=request.user.username)

        try:
            post.voted_users.get(username=current_user.username)
        except blog.models.BlogUser.DoesNotExist:
            if request.POST.get('plus'):
                post.like(current_user)
            else:
                post.dislike(current_user)
        finally:
            return ObjectDetailMixin.get(self, request, slug)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_object = bound_form.save()
            new_object.author = BlogUser.objects.get(username=request.user.username)
            new_object.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': bound_form})


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    redirect_view = 'posts_list_url'
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
    redirect_url = 'tags_list_url'
    model = Tag
    model_form = TagForm
    template = 'blog/tag_delete_form.html'
    raise_exception = True


class UserCreate(ObjectCreateMixin, View):
    model = BlogUser
    model_form = UserForm
    template = 'blog/user_sign_up_form.html'

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            password = request.POST.get('password', False)
            new_object = bound_form.save()
            User.set_password(new_object, password)
            new_object.save()

            return redirect(new_object)
        return render(request, self.template, context={'form': bound_form})


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


def logout_view(request):
    logout(request)
    return redirect('posts_list_url')


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


def users_list(request):
    users = BlogUser.objects.all()
    return render(request, 'blog/users_list.html', context={'users': users, 'count': BlogUser.objects.count()})
