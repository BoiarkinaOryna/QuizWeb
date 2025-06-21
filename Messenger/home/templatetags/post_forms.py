from django import template
from ..models import Post

register = template.Library()

@register.inclusion_tag('inclusion_tags/post_form_tag.html', takes_context=True)
def form_for_post(context: dict, post = ""):
    return {
        "post": post,
        'form': context.get("form"),
    }