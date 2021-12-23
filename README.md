# django-infinite-scroll
Add infinite scroll to any django app.

## Features

    - Allows to add infinite scroll to any page.
    - Works with Django's Queryset and regular lists.
    - Easy to install and set up.
    - Requires no aditional javascript framework.

## Quicksetup

With docker compose:

``` bash
    git clone https://github.com/gsteixeira/django-infinite-scroll.git
    cd django-infinite-scroll/example
    docker-compose up
```

Go to http://localhost:8000 and try it out. 8)


## installation

Install module.

```bash
    pip install django-infinite-scroll
```

Add to settings.py

```python
    INSTALLED_APPS = [
        # ...
        'compressor',
        'infscroll',
    ]
    # we use django-compressor so you need to set up the STATIC_ROOT
    STATIC_ROOT = BASE_DIR / "static_root/"
```

First, let's make a view that will load the dynamic content:

```python
    def more(request):
        # This is the list that will be paginated
        list_items = MyModel.objects.all()
        # extra data to pass to the view (optional)
        data = {'foo': 'bar'}
        # Your template (optional)
        template = 'more.html'
        return more_feed(request, list_items, template, extra_data=data)
```

Add it to urls.py

```python
    path('more/', myapp.views.more, name='more'),
```

Finally, Add to the view you want to show the infinite scroll:

```python
    def my_view(request):
        # The list of items to be paginated. It can be any list of queryset.
        list_items = MyModel.objects.all()
        # Get initial data and a first burst of paginated items to show
        paginated = get_feed_pagination(request, list_items)
        data = {
            # we must declare the url where it will load more stuff
            'more_posts_url': reverse('more'),
            }
        # update with paginated info
        data.update(paginated)
        return render(request, 'home.html', data)
```

Now add to your template:

```html
    <html>
        <body>
            <p>Hello</p>
            <!-- The dynamically loaded items will show here -->
            {% include 'infscroll/scroll_box.html' %}
            <!-- This can go in the end of the template -->
            {% include 'infscroll/scroll.html' %}
        </body>
    </html>
```

Now go to the page of "my_view", and you should have infinite scroll!

### (optional) If you want to use a custom "load_more" template

Here is an example:

```html
    {% for item in feed %}
        {{ item }}
    {% endfor %}
    {% include 'infscroll/scroll_tags.html' %}
```
Just add this *for loop* to iterate the list and include the scroll tags


## Settings

    PAGINATION_STEPS - the amount of items each step will load. Default to 10.

## Requirements

    - python3
    - django
    - django-compressor
