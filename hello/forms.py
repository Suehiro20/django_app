from django import forms
from .models import Friend, Message

class FirstForm(forms.Form):
    name = forms.CharField(label='name')
    mail = forms.EmailField(label='mail')
    age = forms.IntegerField(label='age')

class SecondForm(forms.Form):
    check = forms.BooleanField(label='Checkbox', required=False)

class ThirdForm(forms.Form):
    check = forms.NullBooleanField(label='Check')

class FourthForm(forms.Form):
    data = [
        ('値', 'ラベル'),
        ('one', 'item 1'),
        ('two', 'item 2'),
    ]
    choice = forms.ChoiceField(label='Choice', choices=data)

class FifthForm(forms.Form):
    data = [
        ('値', 'ラベル'),
        ('one', 'item 1'),
        ('two', 'item 2'),
    ]
    choice = forms.ChoiceField(label='Radio', choices=data, widget=forms.RadioSelect())

class SixthForm(forms.Form):
    data = [
        ('値', 'ラベル'),
        ('one', 'item 1'),
        ('two', 'item 2'),
    ]
    choice = forms.ChoiceField(label='List', choices=data, widget=forms.Select(attrs={'size': 3}))

class HelloForm(forms.Form):
    data = [
        ('値', 'ラベル'),
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3'),
        ('four', 'item 4'),
        ('five', 'item 5'),
    ]
    choice = forms.MultipleChoiceField(label='Multiple', choices=data, widget=forms.SelectMultiple(attrs={'size': 5}))

class IdForm(forms.Form):
    id = forms.IntegerField(label='ID')

class Create(forms.Form):
    name = forms.CharField(label='Name')
    mail = forms.EmailField(label='Email')
    gender = forms.NullBooleanField(label='Gender')
    age = forms.IntegerField(label='Age')
    birthday = forms.DateField(label='Birth')

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name','mail','gender','age','birthday']

class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)

class CheckForm(forms.Form):
    str = forms.CharField(label='String')

    def clean(self):
        cleaned_data = super().clean()
        str = cleaned_data['str']
        if (str.lower().startswith('no')):
            raise forms.ValidationError('You input "NO"!')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'friend']