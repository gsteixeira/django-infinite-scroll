from django.shortcuts import render
from infscroll.utils import get_pagination, PAGINATION_STEPS

def more_items(request, feed:list,
               template:str='infscroll/more.html',
               extra_data:dict={},
               steps:int=PAGINATION_STEPS,
               minimum:int=0,
               shuf:bool=False,
               forever:bool=True):
    """ 
    Renders a page with the next round of items in pagination. 
    To be used with ajax calls
    """
    data = get_pagination(request, feed, pagination_steps=steps,
                          minimum=minimum, shuf=shuf, forever=forever)
    data.update(extra_data)
    return render(request, template, data)
