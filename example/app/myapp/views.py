from django.shortcuts import render
from django.urls import reverse
from infscroll.utils import get_feed_pagination
from infscroll.views import more_feed
#
UPTO = 100

def home(request):
    """ Just a sample page """
    list_items = list(range(UPTO))
    page_canonical = request.GET.get('page', None)
    shuf = request.GET.get('shuffle', False)
    paginated = get_feed_pagination(request,
                                    list_items,
                                    page_canonica=page_canonical,
                                    shuf=shuf)
    data = {
        # we must declare the url where it will load more stuff
        'more_posts_url': reverse('more'),
        }
    # update with paginated info
    data.update(paginated)
    return render(request, 'home.html', data)

def more(request):
    """ This is the view that dynamically loads more content """
    list_items = list(range(UPTO))
    return more_feed(request, list_items, 'more.html')
