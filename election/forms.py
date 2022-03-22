from django import forms

from .models import *

from django.utils import timezone


class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        exclude = ['nb_voix']


class BureauForm(forms.ModelForm):
    class Meta:
        model = Bureau
        fields = ('nom', 'lieu')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')


class ElecteurForm(forms.ModelForm):
    class Meta:
        model = Electeur
        fields = ('date_naissance', 'lieu_naissance', 'numero_cni', 'bureau', 'user')

    def get_age(self, born):
        date_jour = timezone.now()
        return date_jour.year - born.year - ((date_jour.month, date_jour.day) < (born.month, born.day))

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data['date_naissance']
        if self.get_age(date_naissance) < 18:
            raise forms.ValidationError('Désolé mais vous n\'êtes pas encore majeur!')
        return date_naissance


ElecteurFormSet = forms.inlineformset_factory(User, Electeur, form=ElecteurForm, can_delete=False, extra=1)


class VoteForm(forms.Form):
    candidats = forms.ModelChoiceField(queryset=Candidat.objects.all())