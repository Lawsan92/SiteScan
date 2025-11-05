from django import forms

class SiteScanForm(forms.Form):
    user_zip = forms.CharField(label='search ZIP',  max_length=5)