from django import forms

class SearchForm(forms.Form):
    address = forms.CharField(label='address', max_length=100,
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Search for an address...'}))