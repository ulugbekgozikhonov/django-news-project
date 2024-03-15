from django.urls import path
from news_app.views import news_list, news_detail, SearchResultList
from news_app.views import NewsListView, NewsDetailView, home_page_view, ContactPageView, HomePageView, NewsDeleteView, \
    NewsUpdateView, NewsCreateView, admin_page_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', NewsListView.as_view(), name="all_news_list"),
    path('news/create', NewsCreateView.as_view(), name='news_create'),
    # path('news/<slug:news>/', NewsDetailView.as_view(), name='news_detail_page'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('news/<slug:news>/delete', NewsDeleteView.as_view(), name='news_delete_page'),
    path('news/<slug:news>/edit', NewsUpdateView.as_view(), name='news_edit_page'),
    path('contact-as/', ContactPageView.as_view(), name='contact_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/',SearchResultList.as_view(),name='search_result')
]
