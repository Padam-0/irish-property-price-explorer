# from django import forms
import floppyforms as forms

class InputForm(forms.Form):

    COUNTY_CHOICES = (
        ('Galway City', 'Galway City'), ('Galway County', 'Galway County'),
        ('Leitrim', 'Leitrim'), ('Mayo', 'Mayo'), ('Roscommon', 'Roscommon'),
        ('Sligo', 'Sligo'), ('Carlow', 'Carlow'), ('Dublin', 'Dublin'), ('Kildare', 'Kildare'),
        ('Kilkenny', 'Kilkenny'), ('Laois', 'Laois'), ('Longford', 'Longford'), ('Louth', 'Louth'),
        ('Meath', 'Meath'), ('Offaly', 'Offaly'), ('Westmeath', 'Westmeath'),
        ('Wexford', 'Wexford'), ('Wicklow', 'Wicklow'), ('Clare', 'Clare'),
        ('Cork City', 'Cork City'), ('Cork County', 'Cork County'), ('Kerry', 'Kerry'),
        ('Limerick City', 'Limerick City'), ('Limerick County', 'Limerick County'),
        ('Tipperary', 'Tipperary'),  ('Waterford City', 'Waterford City'),
        ('Waterford County', 'Waterford County'), ('Cavan', 'Cavan'), ('Donegal', 'Donegal'),
        ('Monaghan', 'Monaghan')
    )

    DOP_CHOICES = (
        ('Semi-Detached House', 'Semi-Detached House'),
        ('Detached House', 'Detached House'),
        ('Terraced House', 'Terraced House'),
        ('End of Terrace House', 'End of Terrace House'),
        ('Townhouse', 'Townhouse'), ('Other', 'Other')
    )

    CONDITION_CHOICES = (
        ('Second-Hand House / Apartment', 'Second-Hand House / Apartment'),
        ('New House / Apartment', 'New House / Apartment')
    )

    address = forms.CharField(label='address', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please enter your address...'}))
    # county = forms.ChoiceField(label='county', choices=COUNTY_CHOICES)

    county = forms.widgets.Input(datalist=COUNTY_CHOICES, template_name='floppyforms/input.html')

    type = forms.ChoiceField(label='type', choices=DOP_CHOICES)
    condition = forms.ChoiceField(label='condition', choices=CONDITION_CHOICES)

    BED_BATH_CHOICES = (
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
        (9, 9), ('10+', '10+')
    )
    bed = forms.ChoiceField(label='county', choices=BED_BATH_CHOICES)
    bath = forms.ChoiceField(label='county', choices=BED_BATH_CHOICES)