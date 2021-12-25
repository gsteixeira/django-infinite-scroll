from django.shortcuts import render
from django.urls import reverse
from infscroll.utils import get_pagination
from infscroll.views import more_items
#
UPTO = 100
FOREVER = True

def home(request):
    """ Just a sample page """
    list_items = list(range(UPTO))
    paginated = get_pagination(request, list_items,
                               page_canonical=request.GET.get('page', None),
                               forever=FOREVER,
                               shuf=request.GET.get('shuffle', False))
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
    return more_items(request, list_items, 'more.html', forever=FOREVER)
