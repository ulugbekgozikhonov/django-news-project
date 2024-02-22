from django.urls import path
# from news_app.views import news_list, news_detail
from news_app.views import NewsListView, NewsDetailView, home_page_view, ContactPageView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', NewsListView.as_view(), name="all_news_list"),
    # path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail_page'),
    path('news/<slug:news>/', NewsDetailView.as_view(), name='news_detail_page'),
    path('contact-as/', ContactPageView.as_view(), name='contact_page'),
]
