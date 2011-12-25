from django.template import Library
from django.conf import settings

register = Library()

@register.filter
def wikifytitle(value):
    """Remove underscores from titles"""
    return value.replace("_", " ")

@register.filter
def wikify(value):
    """Makes WikiWords"""
    import re
    from subkoord.wiki.models import Wikipage
    wikifier = re.compile(r'\[\[(.+?)\]\]')
    titles = wikifier.findall(value)
    if len(titles):
        existing_pages = Wikipage.objects.filter(title__in=titles).only("title")
        for title in titles:
            single_title = re.compile(r'\[\[('+title+')\]\]')
            humanized_title = wikifytitle(title)
            if len(existing_pages.filter(title__exact=title)): page_exists = ""
            else: page_exists = "new_page"
            value = single_title.sub(r'<a href="/wiki/\1/" class="'+page_exists+'">'+humanized_title+'</a>', value)
    return value
