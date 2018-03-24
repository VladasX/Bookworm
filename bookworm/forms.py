from django import forms
from django.contrib.auth.models import User
from bookworm.models import UserProfile, Review, ReadingList

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
	favouriteBook = forms.CharField(required=False)

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
		

#Form for reading list.
class ReadingListForm(forms.ModelForm):
	status = forms.IntegerField(required=False)

	class Meta:
		model = ReadingList
		fields = ('status', )
		
#Form to change a book in the reading list.
class ReadingListFormChange(forms.ModelForm):
	status = forms.IntegerField(required=False)
	bookid = forms.CharField(required=False)
	pages = forms.IntegerField(required=False)

	class Meta:
		model = ReadingList
		fields = ('status', )