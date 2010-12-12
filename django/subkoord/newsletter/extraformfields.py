#http://djangosnippets.org/snippets/1663/
from django import forms

class FeaturedModelChoiceIterator(object):
    # Adapted from django.forms.models.ModelChoiceIterator
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset
        self.featured_queryset = field.featured_queryset

    def __iter__(self):
        # Just show all the featured content
        for obj in self.featured_queryset.all():
            yield self.choice(obj)
        # Add the empty label between featured and non-featured content
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        # And here is the non-featured content
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.all():
                yield self.choice(obj)

    def choice(self, obj):
        if self.field.to_field_name:
            key = obj.serializable_value(self.field.to_field_name)
        else:
            key = obj.pk
        return (key, self.field.label_from_instance(obj))

class FeaturedModelChoiceField(forms.ModelChoiceField):
    """ This is just like a model choice field, but will add a set of "featured"
        choices to the top of the list. These choices are provided by the
        featured_queryset parameter.
    """
    def __init__(self, featured_queryset, *args, **kwargs):
        self.featured_queryset = featured_queryset
        super(FeaturedModelChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        # NB this method is not in the public Django API.

        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh QuerySetIterator that has not been
        # consumed. Note that we're instantiating a new QuerySetIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return FeaturedModelChoiceIterator(self)
    choices = property(_get_choices, forms.ChoiceField._set_choices)

    def _get_featured_queryset(self):
        return self._featured_queryset

    def _set_featured_queryset(self, queryset):
        self._featured_queryset = queryset
        self.widget.choices = self.choices
