from django import forms

from .models import UserInfo, UserProfile, Education, WorkExperience, Skills, Training, SocialAccount

class UserSignupForm(forms.ModelForm):

	password= forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget = forms.PasswordInput)

	class Meta:

		model = UserInfo
		fields = ["email",]

	def clean(self):

		cleaned_data = super(UserSignupForm, self).clean()
		
		password1 = cleaned_data.get("password")
		password2 = cleaned_data.get("confirm_password")

		if password1 and password2 and password1 != password2:
			self.add_error('confirm_password', "Password does not match")
		
		return cleaned_data

class UserLoginForm(forms.Form):

	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

	
