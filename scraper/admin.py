from django.contrib import admin

from scraper.models import Keyword, KeywordResult

# Register your models here.
admin.site.register(Keyword)
admin.site.register(KeywordResult)