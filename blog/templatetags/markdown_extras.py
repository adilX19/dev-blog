from django import template
from django.template.defaultfilters import stringfilter
from blog.models import SavedPost

import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
	return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter()
@stringfilter
def saved(post, user):
	return SavedPost.objects.filter(author=user, post=post).exists()