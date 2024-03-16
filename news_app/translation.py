from modeltranslation.translator import register, TranslationOptions, translator
from news_app.models import Category, News


# 1-uslul
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


# 2-usul
# translator.register(News, NewsTranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
