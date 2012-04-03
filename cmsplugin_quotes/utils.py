import os
import glob
from django.conf import settings
from django.forms.forms import pretty_name


def template_choices():

    app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    templates = []
    names = set()

    # project template dirs
    dirs = [os.path.join(dir, app_name)
            for dir in settings.TEMPLATE_DIRS
            if os.path.isdir(os.path.join(dir, app_name))]

    if not dirs:
        #application template dirs
        dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', app_name)
        if os.path.isdir(dir):
            dirs.append(dir)

    for dir in dirs:
        found = glob.glob(os.path.join(dir, '*.html'))
        for tpl in found:
            dir, file = os.path.split(tpl)
            base, ext = os.path.splitext(file)
            key, name = os.path.join(dir.split('/')[-1], file), pretty_name(base)
            if name not in names:
                names.add(name)
                templates.append((key, name))
    return sorted(templates)
