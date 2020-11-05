from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext_lazy as _

from wishes.models import Family, Member, Wish


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        labels = {
            'name': _('Nazwa rodziny'),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user', 'family', 'main_member']
        labels = {
            'name': _('Imię'),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Taki członek rodziny już istnieje!",
            }
        }



class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = '__all__'
        labels = {
            'name': _('Co chcesz dostać?'),
            'description': _('Opowiedz coś więcej ;)'),
            'link': _('A może masz upatrzony już konkretny model? Wrzuć nam linka ;)'),
            'member': _('Wybierz członka rodziny, którego to życzenie :) (jeśli go tu nie ma, musisz go najpierw dodać!')
        }

