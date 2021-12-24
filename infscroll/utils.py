from random import shuffle
from django.conf import settings

PAGINATION_STEPS = getattr(settings, 'PAGINATION_STEPS', 10)

def get_pagination(request, feed:list,
                   pagination_steps:int=PAGINATION_STEPS,
                   minimum:int=0,
                   page_canonica:int=None,
                   shuf:bool=False) -> dict:
    """ Prepare data to send html in order to keep a syncronized pagination
    """
    has_newer_posts = True
    has_older_posts = True
    if 'view-all' in request.GET.keys():
        pagination_steps=len(feed)
    if page_canonica:
        current_page_canonica = int(page_canonica) * pagination_steps
        page = int(current_page_canonica)
    else:
        page = num_only(request.GET.get('page', 0))
        page_canonica = int(page / pagination_steps)
    older_posts = page + pagination_steps
    newer_posts = page - pagination_steps
    if page <= 0:
        newer_posts = 0
        page = 0
        has_newer_posts = False
    feed_count = len(feed)
    feed = feed[page:older_posts]
    if feed_count <= older_posts:
        has_older_posts = False
        older_posts = 0
    should_load_more = (feed_count >= minimum)
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
        'page_canonica': page_canonica,
        'older_posts_canonica': int(older_posts / pagination_steps),
        'newer_posts_canonica': int(newer_posts / pagination_steps),
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

