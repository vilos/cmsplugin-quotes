from random import randint
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from models import Quote, QuotePlugin


START_VAR = 'start'

class RotatingQuotes(CMSPluginBase):
    '''
    '''
    model = QuotePlugin
    name = _("Rotating Quotes")
    module = _("Quotes")

    def render(self, context, instance, placeholder):
        """ """

        request = context['request']

        self.render_template = instance.template

        # number of quotes to display
        count = instance.count
        # number of quotes in db
        base = Quote.objects.by_tag(instance.tag)
        n = len(base)
        count = min(n, count)

        quotes = []
        next = n
        if count > 0:
            try:
                a = int(request.GET.get(START_VAR, -1))
            except ValueError:
                a = -1
            if a < 0:
                a = randint(0, max(n-1,0))

            # max index
            b = (a + count) % n
            next = b #(b + 1) % n

            if b > a:
                quotes = base[a:b]
            else:
                quotes = base[a:] + base[:b]

        context.update({
            'object':instance,
            'placeholder':placeholder,
            'quotes':quotes,
            'next': next
        })
        return context

plugin_pool.register_plugin(RotatingQuotes)