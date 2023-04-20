from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import PostForm, ReplyForm
from .models import Post, Reply, News


class PostList(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    template_name = 'board/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    form_class = ReplyForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            post = self.get_object()
            context['replies'] = Reply.objects.filter(
                post=post,
                author=self.request.user
            )
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=self.get_form())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            post = self.object
            send_mail(
                subject=f"Новый отклик на ваше объявление '{post}'",
                message=f"{post.author}, вы получили новый отклик на ваше "
                        f"объявление '{post}'! Примите его или отклоните!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post.author.email]
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'board/post_create.html'
    form_class = PostForm
    extra_context = {'is_edit': True}


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'board/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'board/profile.html'


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'board/reply_list.html'
    paginate_by = 10
    context_object_name = 'replies'

    def get_queryset(self):
        self.selected_post_id = self.request.GET.get('post_id')
        replies = Reply.objects.filter(post__author=self.request.user)
        if self.selected_post_id:
            return replies.filter(post__id=self.selected_post_id)
        else:
            return replies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_post_id'] = int(self.selected_post_id) if self.selected_post_id else None
        return context

    def post(self, request, *args, **kwargs):
        reply_pk = request.POST.get('pk')
        reply = Reply.objects.get(pk=reply_pk)

        if 'accept' in request.POST:
            reply.status = 'A'
        elif 'reject' in request.POST:
            reply.status = 'R'

        reply.save()
        mail = send_mail(
            subject=f"Реакция на ваш отклик по объявлению '{reply.post}'",
            message=f"{reply.author}!\n\nВаш отклик '{reply}' на объявление '{reply.post}' "
                    f"{reply.get_status_display().lower()}!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reply.author.email]
        )
        print(mail)
        return redirect(self.request.path_info)


class NewsList(ListView):
    model = News
    template_name = 'board/news_list.html'
    queryset = News.objects.all()
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    model = News
    template_name = 'board/news_detail.html'
    context_object_name = 'news'
