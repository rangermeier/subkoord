# http://djangosnippets.org/snippets/2145/
import os
import os.path
import re
import Image
from django.template import Library

register = Library()

def thumbnail(file, size='100x100x1'):
    # defining the size
    x, y, ratio = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, 'thumbnails', miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = '/'.join((filehead, 'thumbnails', miniature))
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename) and os.path.exists(file.path) :
        image = Image.open(filename)
        if ratio == 0:
            image = image.resize([x, y], Image.ANTIALIAS)
        else:
            image.thumbnail([x, y], Image.ANTIALIAS)        
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url


register.filter(thumbnail)

