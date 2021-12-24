from django.test import TestCase

from infscroll.utils import get_pagination, num_only
from infscroll.views import more_items

class FakeRequest(object):
    def __init__(self, get={}):
        self.GET = get

# Create your tests here.
class InfiniteScrollTestCase(TestCase):
    def setUp(self):
        self.feed = list(range(100))

    def test_get_pagination(self):
        """ test the initial pagination step """
        request = FakeRequest()
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), 10)
        i = 0
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1
        self.assertEqual(data['page'], 0)
        self.assertEqual(data['older_posts'], 10)
        self.assertEqual(data['newer_posts'], 0)
        self.assertEqual(data['has_newer_posts'], False)
        self.assertEqual(data['has_older_posts'], True)
        self.assertEqual(data['should_load_more'], True)
        self.assertEqual(data['page_canonica'], 0)
        self.assertEqual(data['older_posts_canonica'], 1)
        self.assertEqual(data['newer_posts_canonica'], 0)

    def test_get_pagination_goes_up(self):
        """ test what would be the second loaded page """
        request = FakeRequest({'page': '20'})
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), 10)
        i = 20
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1
        self.assertEqual(data['page'], 20)
        self.assertEqual(data['older_posts'], 30)
        self.assertEqual(data['newer_posts'], 10)
        self.assertEqual(data['has_newer_posts'], True)
        self.assertEqual(data['has_older_posts'], True)
        self.assertEqual(data['should_load_more'], True)
        self.assertEqual(data['page_canonica'], 2)
        self.assertEqual(data['older_posts_canonica'], 3)
        self.assertEqual(data['newer_posts_canonica'], 1)

    def test_get_pagination_canonica(self):
        """ check the pagination when the canonical number is called
        Eg. Page 2 should load from 20 to 30
        """
        request = FakeRequest()
        data = get_pagination(request, self.feed,
                              page_canonica=2,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), 10)
        i = 20
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1
        self.assertEqual(data['page'], 20)
        self.assertEqual(data['older_posts'], 30)
        self.assertEqual(data['newer_posts'], 10)
        self.assertEqual(data['has_newer_posts'], True)
        self.assertEqual(data['has_older_posts'], True)
        self.assertEqual(data['should_load_more'], True)
        self.assertEqual(data['page_canonica'], 2)
        self.assertEqual(data['older_posts_canonica'], 3)
        self.assertEqual(data['newer_posts_canonica'], 1)

    def test_get_pagination_end_of_list(self):
        """ Test the behavior when we get to the end of our list.
        Eg. From a list of 100 items, the end is 90 to 99
        """
        request = FakeRequest({'page': '90'})
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), 10)
        i = 90
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1
        self.assertEqual(data['page'], 90)
        self.assertEqual(data['older_posts'], 0)
        self.assertEqual(data['newer_posts'], 80)
        self.assertEqual(data['has_newer_posts'], True)
        self.assertEqual(data['has_older_posts'], False)
        self.assertEqual(data['should_load_more'], True)
        self.assertEqual(data['page_canonica'], 9)
        self.assertEqual(data['older_posts_canonica'], 0)
        self.assertEqual(data['newer_posts_canonica'], 8)

    def test_get_pagination_off_the_list(self):
        """ Test when we end our list but there is less than a page of items.
        Eg. Our list has 100 items, If we start at 95 it should be from 95 to 99
        """
        request = FakeRequest({'page': '95'})
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), 5)
        i = 95
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1
        self.assertEqual(data['page'], 95)
        self.assertEqual(data['older_posts'], 0)
        self.assertEqual(data['newer_posts'], 85)
        self.assertEqual(data['has_newer_posts'], True)
        self.assertEqual(data['has_older_posts'], False)
        self.assertEqual(data['should_load_more'], True)
        self.assertEqual(data['page_canonica'], 9)
        self.assertEqual(data['older_posts_canonica'], 0)
        self.assertEqual(data['newer_posts_canonica'], 8)

    def test_get_pagination_view_all(self):
        """ Test when the ?view-all flag is set. Should disable pagination """
        request = FakeRequest({'view-all': None})
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        self.assertEqual(len(data['feed']), len(self.feed))
        i = 0
        for item in data['feed']:
            assert self.feed[i] == item
            i += 1

    def test_get_pagination_shuffle(self):
        """ test when we ask to shuffle the array """
        request = FakeRequest()
        data = get_pagination(request, self.feed,
                              pagination_steps=10,
                              shuf=True)
        self.assertEqual(len(data['feed']), 10)
        for item in data['feed']:
            assert item in self.feed[0:10]

    def test_view_more_items(self):
        """ test the view that loads more items """
        request = FakeRequest()
        response = more_items(request, self.feed)
        self.assertEqual(response.status_code, 200)
        data = get_pagination(request, self.feed,
                              pagination_steps=10)
        content = str(response.content)
        for item in data['feed']:
            self.assertIn(str(item), content)

    def test_num_only(self):
        """ unitary test for the function num_only """
        assert num_only(35) == 35
        assert num_only("35") == 35
        assert num_only("3.5") == 35
        assert num_only("3a$d5") == 35
        assert num_only(0) == 0
        assert num_only("0") == 0
        assert num_only("") == None
        assert num_only(" ") == None
