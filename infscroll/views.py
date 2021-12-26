from django.shortcuts import render
from infscroll.utils import get_pagination, PAGINATION_STEPS, MINIMUN_ITEMS

def more_items(request, feed:list,
               template:str='infscroll/more.html',
               extra_data:dict={},
               steps:int=PAGINATION_STEPS,
               minimum:int=MINIMUN_ITEMS,
               shuf:bool=False,
               forever:bool=True):
    """ 
    Renders a page with the next round of items in pagination. 
    To be used with ajax calls

    :param request HttpRequest: the request
    :param pagination_steps int: how many items will load for each page.
    :param minimum int: the minimum amount of items in the list to trigger
    :param page_canonical int: the absolute page number.
                                eg.Page 2 is from 20 to 30.
    :param shuf bool: if we should shuffle the array.
    :param forever bool: If this is true, when we get at the end of the list,
                         start from the begining.
    """
    data = get_pagination(request, feed, pagination_steps=steps,
                          minimum=minimum, shuf=shuf, forever=forever)
    data.update(extra_data)
    return render(request, template, data)
