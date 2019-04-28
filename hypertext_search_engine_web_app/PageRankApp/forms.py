from django import forms


class SearchForm(forms.Form):
    searched_exp = forms.CharField(label='', max_length=100, required=False)
