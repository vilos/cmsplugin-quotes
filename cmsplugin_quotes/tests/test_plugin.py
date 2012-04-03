from django.utils import unittest
from django import http
from cmsplugin_quotes.cms_plugins import RotatingQuotes, START_VAR
from cmsplugin_quotes.models import Quote


class DummyRequest(http.HttpRequest):
    def __init__(self, GET=None):
        super(DummyRequest, self).__init__()
        self.method = GET and "GET" or "POST"
        if GET is not None:
            self.GET.update(GET)
        self._dont_enforce_csrf_checks = True

class DummyContext(dict):
    def __init__(self, query=None):
        request = DummyRequest(GET=query)
        self.update(dict(request=request))

class DummyInstance(object):
    count = 5


class DummyPlaceholder(object):
    pass


class RoundaboutTestCase(unittest.TestCase):

    N = 20

    def setUp(self):


        n = Quote.objects.count()
        if n == 0:
            for idx in range(self.N):
                kw = dict( author=str(idx),
                           text=chr(ord('a') + idx))

                Quote.objects.create(**kw)
        else:
            print "%d items already exists." % n

    def testRender(self):

        plugin = RotatingQuotes()
        instance = DummyInstance()
        data = plugin.render(DummyContext(), instance, DummyPlaceholder())

        quotes = data['quotes']
        next = data['next']

        self.failUnless(len(quotes)==instance.count)

        idx = -1
        for quote in quotes:
            a = int(quote.author)
            msg = "a: %d, idx: %d" % (a, idx)
            if idx >= 0:
                if a == 0:
                    self.failUnless(idx==(self.N-1), msg)
                else:
                    self.failUnless((a-idx) == 1, msg)
            idx = a

        last = int(quotes[-1].author)
        if last == self.N - 1:
            x = 0
        else:
            x = last+1

        self.failUnless(next == x, "next: %d, x: %d" % (next, x))

    def testRange(self):
        plugin = RotatingQuotes()
        instance = DummyInstance()
        for idx in range(20):
            q = {START_VAR: idx}
            data = plugin.render(DummyContext(q), instance, DummyPlaceholder())
            quotes = data['quotes']
            next = data['next']
            print "start: %d, next: %s" % (idx, next),
            print quotes

            self.failUnless(len(quotes)==instance.count)
