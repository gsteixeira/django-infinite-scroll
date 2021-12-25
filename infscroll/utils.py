from random import shuffle
from django.conf import settings
try: # python >=3.8
    from importlib.metadata import version as get_version
except: # python < 3.8
    from pkg_resources import get_distribution as get_version

INFSCROLL_VERSION = get_version('django-infinite-scroll')
PAGINATION_STEPS = int(getattr(settings, 'PAGINATION_STEPS', 10))

def get_pagination(request, feed:list,
                   pagination_steps:int=PAGINATION_STEPS,
                   minimum:int=0,
                   page_canonical:int=None,
                   shuf:bool=False,
                   forever:bool=True) -> dict:
    """ Prepare data to send html in order to keep a syncronized pagination.
    :param request HttpRequest: the request
    :param pagination_steps int: how many items will load for each page.
    :param minimum int: the minimum amount of items in the list to trigger
    :param page_canonical int: the absolute page number.
                                eg.Page 2 is from 20 to 30.
    :param shuf bool: if we should shuffle the array.
    :param forever bool: If this is true, when we get at the end of the list,
                         start from the begining.
    """
    has_newer_posts = True
    has_older_posts = True
    if 'view-all' in request.GET.keys():
        pagination_steps=len(feed)
    if page_canonical:
        current_page_canonical = int(page_canonical) * pagination_steps
        page = int(current_page_canonical)
    else:
        page = num_only(request.GET.get('page', 0))
        page_canonical = int(page / pagination_steps)
    older_posts = page + pagination_steps
    newer_posts = page - pagination_steps
    if page <= 0:
        newer_posts = 0
        page = 0
        has_newer_posts = False
    feed_count = len(feed)
    feed = feed[page:older_posts]
    should_load_more = (feed_count >= minimum)
    # This means we reached the end of the list
    if feed_count <= older_posts:
        has_older_posts = False
        older_posts = 0
        should_load_more = (should_load_more and forever)
    if shuf:
        feed = list(feed)
        shuffle(feed)
    data = {
        'feed': feed,
        'page': page,
        'older_posts': older_posts,
        'newer_posts': newer_posts,
        'has_newer_posts': has_newer_posts,
        'has_older_posts': has_older_posts,
        'should_load_more': should_load_more,
        'page_canonical': page_canonical,
        'older_posts_canonica': int(older_posts / pagination_steps),
        'newer_posts_canonica': int(newer_posts / pagination_steps),
        'infscroll_version': INFSCROLL_VERSION,
        }
    return data

def num_only(value:any)->int:
    """ extract non digits from a string and return integer """
    value = str(value)
    nlist = [num for num in value if num.isdigit()]
    if nlist:
        return int(''.join(nlist))
    else:
        return None

