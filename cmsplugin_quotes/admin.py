from django.contrib import admin
from models import Quote


class QuoteOptions(admin.ModelAdmin):
    list_display = ('author', 'get_tags', 'excerpt', 'active')
    list_display_links = ('author',)
    list_filter = ('tags',)


admin.site.register(Quote, QuoteOptions)
