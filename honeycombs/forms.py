from django.forms import ModelForm

from honeycombs.models import Honeycombs


class HoneycombsForm(ModelForm):
    class Meta:
        model = Honeycombs
        fields = ('name', 'topic', 'description', 'image', 'paid_content',)
