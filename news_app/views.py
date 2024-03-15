from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from config.custom_permissions import OnlyLoggedSuperUser
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, DeleteView, UpdateView, CreateView

from news_app.models import News, Category
from news_app.forms import ContactForm, CommentForm

# Create your views here.
""" WITH FUNCTIONS VIEWS """


def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }

    return render(request=request, template_name='news/news_list.html', context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    """ko'rishlar soni >>> 1-usul mosir"""
    # news.view_count = news.view_count+1
    # news.save()
    """ko'rishlar soni 2-usul bitta clas yaratamiz va uni ichida api addres bo'ladi
     lekin tayyor qilb bizda djangoni o'zini hitcount modeli bot tashi kutibxona
     pipenv install django-hitcount  class viewga asoslagan bo'lsa yaxshi bo'ladi
     lekin biz defda qilamiz"""
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'news_comment': new_comment,
        'comment_form': comment_form,
        'comment_count': comments_count,

    }

    return render(request=request, template_name='news/news_detail.html', context=context)


"""WITH CLASS VIEWS"""


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.published.all()


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'news'

    def get_queryset(self):
        return News.published.all()


def home_page_view(request):
    news_list = News.published.all().order_by("-publish_time")[:15]
    categories = Category.objects.all()
    local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[0]
    local_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[1:6]

    context = {
        'news_list': news_list,
        'categories': categories,
        'local_one': local_one,
        'local_news': local_news,
    }

    return render(request=request, template_name='news/index.html', context=context)


class HomePageView(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by("-publish_time")[:4]
        context['local_news'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:5]
        return context


# def contact_page_view(request):
#
#     form = ContactForm(request.POST or None)
#
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>THANKS</h2>")
#
#     context = {
#         "form": form
#     }
#
#     return render(request=request, template_name='news/pages/contact.html', context=context)


class ContactPageView(TemplateView):
    template_name = 'news/pages/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }

        return render(request, 'news/pages/contact.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)

        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Thanks bro</h2>")
        context = {
            "form"
        }

        return render(request, 'news/pages/contact.html', context)


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ("title", 'body', 'image', 'category', 'status')
    template_name = "news/crud/update.html"
    slug_url_kwarg = 'news'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = "news/crud/delete.html"
    success_url = reverse_lazy('home_page')
    slug_url_kwarg = 'news'


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'news/crud/creat.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)

    context = {
        'admin_user': admin_user
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            title__icontains=query, body__icontains=query
            # Q(title__icontains=query) | Q(body__icontains=query)
        )
