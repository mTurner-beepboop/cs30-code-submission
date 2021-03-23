from django import forms
from django.contrib.auth.models import User


SCOPE_CHOICES = (("Scope 1", "Scope 1"),
                 ("Scope 2", "Scope 2"),
                 ("Scope 3", "Scope 3"),
                 ("Outside of Scopes", "Outside of Scopes")
                 )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


#Examin if the constraints here are correct, and ensure they are also correct in edit.html
class EditForm(forms.Form):
    scope = forms.ChoiceField(choices = SCOPE_CHOICES)
    level1 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level2 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level3 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level4 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level5 = forms.CharField(max_length = 30, min_length = 1, required=False)
    ef = forms.FloatField(max_value = 99999, min_value = 0.000001)
    cu = forms.CharField(max_length = 30)
    preference =  forms.IntegerField(min_value = 0, max_value=2)
    source = forms.CharField(max_length = 30)

class UploadForm(forms.Form):
    ref_num = forms.IntegerField(min_value = 0, max_value = 99999)
    scope = forms.ChoiceField(choices = SCOPE_CHOICES)
    level1 = forms.CharField(max_length = 30, min_length = 1)
    level2 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level3 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level4 = forms.CharField(max_length = 30, min_length = 1, required=False)
    level5 = forms.CharField(max_length = 30, min_length = 1, required=False)
    ef = forms.FloatField(max_value = 99999, min_value = 0)
    cu = forms.CharField(max_length = 30)
    preference =  forms.IntegerField(min_value = 0, max_value=2)
    source = forms.CharField(max_length = 30)
