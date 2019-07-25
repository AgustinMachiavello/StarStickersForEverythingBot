from django import forms


class SecretCodeForm(forms.Form):
	secret_code = forms.FloatField(min_value=0, label="", widget=forms.TextInput(
		attrs={
			'class': '',
			'type': 'password',
			'placeholder': 'Your code here uwu',
		}
	))