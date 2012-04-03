from datetime import datetime
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_unicode
from django.utils.translation import gettext_lazy as _
from cms.models import CMSPlugin
from taggit.models import Tag
from taggit.managers import TaggableManager
from utils import template_choices


def get_choices(self, include_blank=False):
    """Returns choices with a default blank choices included, for use
    as SelectField choices for this field."""
    rel_model = self.rel.to
    return [(getattr(x, self.rel.get_related_field().attname), smart_unicode(x))
                for x in rel_model._default_manager.complex_filter(self.rel.limit_choices_to)]

# hack to get list_filter working with TaggableManager field
setattr(TaggableManager, get_choices.__name__, get_choices)


class QuoteManager(models.Manager):
    def by_id(self, id):
        """Retrieve by ID"""
        return get_object_or_404(self, pk=id)

    def active(self, **kw):
        return self.filter(active=True, **kw).distinct()

    def by_tag(self, tag, **kw):
        if tag is None:
            return self.active(**kw)
        return self.active(tags__name=tag, **kw)


class Quote(models.Model):
    """The quote model."""

    author = models.CharField(_('Author'), max_length=100, blank=False,
        help_text=_("The name of the quote author"))
    text = models.TextField(_('Quote'), blank=False, null=False,
        help_text=_("The quote given."))
    active = models.BooleanField(_("Enabled"), default=True)
    #created = models.DateField(_("Date created"), null=True, blank=True)

    tags = TaggableManager()
    objects = QuoteManager()

    def get_tags(self):
        return u', '.join([tag.name for tag in self.tags.all()])
    get_tags.short_description = 'Tags'

    @property
    def excerpt(self):
        return u"%s..." % self.text[:20]

    def __unicode__(self):
        return u"%s %s" % (self.author, self.excerpt)


class QuotePlugin(CMSPlugin):
    """ """

    count = models.IntegerField(_("count"), help_text=_("Number of displayed quotes"), default=3)
    tag = models.ForeignKey(Tag, help_text=_("Tag to filter quotes against"), blank=True, null=True, related_name='plugins')
    template = models.CharField(_("template"), max_length=100,
                                choices=template_choices(),
                                default=template_choices()[0][0],
                                help_text=_('The template used to render the content.'))

    def __unicode__(self):
        if self.tag:
            return u"%s - %s" % (self.tag, self.count)
        else:
            return u"%s" % self.count
