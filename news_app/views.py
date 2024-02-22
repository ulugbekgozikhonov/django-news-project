from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from news_app.models import News, Category
from news_app.forms import ContactForm

# Create your views here.
""" WITH FUNCTIONS VIEWS """
# def news_list(request):
#     news_list = News.published.all()
#     context = {
#         'news_list': news_list
#     }
#
#     return render(request=request, template_name='news/news_list.html', context=context)
#
#
# def news_detail(request, id):
#     news = get_object_or_404(News, id=id, status=News.Status.Published)
#
#     context = {
#         'news': news
#     }
#
#     return render(request=request, template_name='news/news_detail.html', context=context)

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
