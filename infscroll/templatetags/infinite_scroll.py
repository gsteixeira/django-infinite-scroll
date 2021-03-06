from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(name='set_infinite_scroll', takes_context=True)
def set_infinite_scroll(context):
    """ renders the html to set up and load the necessary JS and CSS.
    This is used by {% set_infinite_scroll %} tag.
    """
    data = get_context_data(context)
    return render_to_string('infscroll/scroll.html', data)

@register.simple_tag(name='infinite_scroll_box', takes_context=True)
def infinite_scroll_box(context):
    """ renders the html that loads the dynamic content.
    This is used by {% infinite_scroll_box %} tag.
    """
    data = get_context_data(context)
    return render_to_string('infscroll/scroll_box.html', data)

@register.simple_tag(name='infinite_scroll_tags', takes_context=True)
def infinite_scroll_tags(context):
    """ renders the html that loads the dynamic content.
    This is used by {% infinite_scroll_box %} tag.
    """
    data = get_context_data(context)
    return render_to_string('infscroll/scroll_tags.html', data)


def get_context_data(context):
    """ Get the correct dictionary from the context.
    Maybe there is a better way to do this...
    """
    for ctx_dict in context.dicts:
        if 'feed' in ctx_dict.keys():
            return ctx_dict
