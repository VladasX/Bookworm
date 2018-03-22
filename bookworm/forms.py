from django import forms
from django.contrib.auth.models import User
from bookworm.models import UserProfile, Review

#Form for user accounts.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

#Form for user profiles.
class UserProfileForm(forms.ModelForm):
	bio = forms.CharField(required=False)
	picture = forms.ImageField(required=False)

	class Meta:
		model = UserProfile
		exclude = ('user',)

#Form for reviews.
class ReviewForm(forms.ModelForm):
	text = forms.CharField(required=False)
	rating = forms.IntegerField(required=False)

	class Meta:
		model = Review
		fields = ('text', 'rating', )